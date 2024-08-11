using SharpCompress.Archives;
using SharpCompress.Archives.Zip;
using SharpCompress.Common;
using SharpCompress.Writers;
using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Windows;
using Microsoft.Win32;
using System.Windows.Controls;
using System.Windows.Forms;

namespace Archive
{
    public partial class MainWindow : Window
    {
        private string _selectedPath;
        private bool _isArchiveSelectionMode;
        private ObservableCollection<FileEntry> _fileEntries = new ObservableCollection<FileEntry>();

        public MainWindow()
        {
            InitializeComponent();
            FilesDataGrid.ItemsSource = _fileEntries;
            UpdateFileStatistics();

            // Подписка на изменения в коллекции для обновления статистики
            _fileEntries.CollectionChanged += (s, e) => UpdateFileStatistics();
        }

        private void BrowseButton_Click(object sender, RoutedEventArgs e)
        {
            if (ExtractRadioButton.IsChecked == true)
            {
                _isArchiveSelectionMode = true;
                var openFileDialog = new Microsoft.Win32.OpenFileDialog
                {
                    Filter = "IMG files (*.img)|*.img|All files (*.*)|*.*",
                    Title = "Выберите архив для извлечения"
                };
                if (openFileDialog.ShowDialog() == true)
                {
                    _selectedPath = openFileDialog.FileName;
                    FolderPathTextBox.Text = _selectedPath;
                    LoadFilesFromArchive(_selectedPath);
                }
            }
            else if (PackRadioButton.IsChecked == true)
            {
                _isArchiveSelectionMode = false;
                var folderDialog = new FolderBrowserDialog();
                if (folderDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    _selectedPath = folderDialog.SelectedPath;
                    FolderPathTextBox.Text = _selectedPath;
                    LoadFilesFromFolder(_selectedPath);
                }
            }
        }

        private void ExecuteButton_Click(object sender, RoutedEventArgs e)
        {
            if (_isArchiveSelectionMode)
            {
                ExtractFiles();
            }
            else
            {
                PackFiles();
            }
        }

        private void ExtractFiles()
        {
            if (string.IsNullOrEmpty(_selectedPath))
            {
                System.Windows.MessageBox.Show("Выберите архив для извлечения.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            string extractFolderPath = Path.Combine(Path.GetDirectoryName(_selectedPath), Path.GetFileNameWithoutExtension(_selectedPath));
            Directory.CreateDirectory(extractFolderPath);

            try
            {
                using (var archive = ArchiveFactory.Open(_selectedPath))
                {
                    foreach (var entry in archive.Entries.Where(entry => !entry.IsDirectory && _fileEntries.FirstOrDefault(f => f.Name == entry.Key)?.IsSelected == true))
                    {
                        string filePath = Path.Combine(extractFolderPath, entry.Key);
                        Directory.CreateDirectory(Path.GetDirectoryName(filePath));
                        using (var entryStream = entry.OpenEntryStream())
                        using (var fileStream = File.Create(filePath))
                        {
                            entryStream.CopyTo(fileStream);
                        }
                    }
                }
                System.Windows.MessageBox.Show("Извлечение завершено.", "Успех", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show($"Ошибка при извлечении архива: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void PackFiles()
        {
            if (string.IsNullOrEmpty(_selectedPath))
            {
                System.Windows.MessageBox.Show("Выберите папку для архивации.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            string folderName = new DirectoryInfo(_selectedPath).Name;
            string newArchivePath = Path.Combine(Path.GetDirectoryName(_selectedPath), $"new_{folderName}.img");

            try
            {
                using (var archive = ZipArchive.Create())
                {
                    var dirInfo = new DirectoryInfo(_selectedPath);
                    foreach (var file in dirInfo.GetFiles("*", SearchOption.AllDirectories))
                    {
                        if (_fileEntries.FirstOrDefault(f => f.Name == file.FullName.Substring(dirInfo.FullName.Length + 1))?.IsSelected == true)
                        {
                            string entryName = file.FullName.Substring(dirInfo.FullName.Length + 1);
                            archive.AddEntry(entryName, file);
                        }
                    }

                    using (var stream = File.Create(newArchivePath))
                    {
                        archive.SaveTo(stream, new WriterOptions(CompressionType.Deflate));
                    }
                }
                System.Windows.MessageBox.Show("Архивирование завершено.", "Успех", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show($"Ошибка при создании архива: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void LoadFilesFromArchive(string archivePath)
        {
            _fileEntries.Clear();
            try
            {
                using (var archive = ArchiveFactory.Open(archivePath))
                {
                    foreach (var entry in archive.Entries.Where(entry => !entry.IsDirectory))
                    {
                        var fileEntry = new FileEntry
                        {
                            Name = entry.Key,
                            Type = Path.GetExtension(entry.Key),
                            Size = FormatSize(entry.Size),
                            IsSelected = false
                        };
                        fileEntry.PropertyChanged += FileEntry_PropertyChanged;
                        _fileEntries.Add(fileEntry);
                    }
                }
                UpdateFileStatistics();
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show($"Ошибка при загрузке файлов из архива: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void LoadFilesFromFolder(string folderPath)
        {
            _fileEntries.Clear();
            try
            {
                var dirInfo = new DirectoryInfo(folderPath);
                foreach (var file in dirInfo.GetFiles("*", SearchOption.AllDirectories))
                {
                    var fileEntry = new FileEntry
                    {
                        Name = file.FullName.Substring(dirInfo.FullName.Length + 1),
                        Type = file.Extension,
                        Size = FormatSize(file.Length),
                        IsSelected = false
                    };
                    fileEntry.PropertyChanged += FileEntry_PropertyChanged;
                    _fileEntries.Add(fileEntry);
                }
                UpdateFileStatistics();
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show($"Ошибка при загрузке файлов из папки: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private string FormatSize(long sizeInBytes)
        {
            if (sizeInBytes < 1024) return $"{sizeInBytes} bytes";
            if (sizeInBytes < 1048576) return $"{sizeInBytes / 1024} KB";
            if (sizeInBytes < 1073741824) return $"{sizeInBytes / 1048576} MB";
            return $"{sizeInBytes / 1073741824} GB";
        }

        private void UpdateFileStatistics()
        {
            TotalFilesTextBlock.Text = _fileEntries.Count.ToString();
            SelectedFilesTextBlock.Text = _fileEntries.Count(f => f.IsSelected).ToString();
        }

        private void FileEntry_PropertyChanged(object sender, PropertyChangedEventArgs e)
        {
            if (e.PropertyName == nameof(FileEntry.IsSelected))
            {
                UpdateFileStatistics();
            }
        }

        private void SelectAllCheckBox_Checked(object sender, RoutedEventArgs e)
        {
            foreach (var fileEntry in _fileEntries)
            {
                fileEntry.IsSelected = true;
            }
        }

        private void SelectAllCheckBox_Unchecked(object sender, RoutedEventArgs e)
        {
            foreach (var fileEntry in _fileEntries)
            {
                fileEntry.IsSelected = false;
            }
        }

        private void RadioButton_Checked(object sender, RoutedEventArgs e)
        {
            _selectedPath = string.Empty;
            FolderPathTextBox.Text = string.Empty;
            _fileEntries.Clear();
            UpdateFileStatistics();
        }
    }

    public class FileEntry : INotifyPropertyChanged
    {
        private bool _isSelected;
        public string Name { get; set; }
        public string Type { get; set; }
        public string Size { get; set; }

        public bool IsSelected
        {
            get { return _isSelected; }
            set
            {
                if (_isSelected != value)
                {
                    _isSelected = value;
                    OnPropertyChanged(nameof(IsSelected));
                }
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
