   M S B A M L   `   `   `  ����  Archive    Archive.MainWindow   5   	   R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	     � Title$)  #Менеджер архивов IMG��5   	   $	��400��6&   $	��600��63   .��5      �  � RowDefinitions 5   
   �� 5      $
��Auto �6   �� 5      $��* �6   �� 5	      $
��Auto �6   .+�5   
   � $��0��6   $��10q�6    � ColumnDefinitions 5      �� 5      $
��Auto �6#   �� 5      $��* �6#   �� 5      $
��Auto �6#   .+�5      �� -   5        $��SelectAllCheckBox��5      $��Выбрать все��60   $��0,0,10,0q�6F   $��Center=�5      5   ;   �� 5      -   5        $��FolderPathTextBox��5      $��1��6/   $
��10,0q�6?    �� 
IsReadOnly . $��Center=�5      �� 5      -   5        $��BrowseButton��5      $��2��6)   $��
Обзор��69   $��10,0,0,0q�6I   $��75��5      $��Center=�6    6;   5       &   System.Windows.Controls.DataGrid  5#   
   -   5        $��FilesDataGrid��5#      $��1��6(      AutoGenerateColumns .  $��10q�6Q      CanUserAddRows .     
IsReadOnly .     SelectionMode$ Extended=�5$   =      SelectionUnit$ FullRow=�5%      	   Columns	 5&      4  .System.Windows.Controls.DataGridCheckBoxColumn  5'      ,  &System.Windows.Controls.DataGridColumn
   Header$
 Выбрать��6)      Width5  /System.Windows.Controls.DataGridLengthConverter$ 50 6Y   1  +System.Windows.Controls.DataGridBoundColumn   Binding 6:   �� *
IsSelected+6Y   0  *System.Windows.Controls.DataGridTextColumn  5(      $
 Имя��6%   $ * 6K    62   �� *Name+6K     5)      $
 Тип файла��6%   $ * 6Q    68   �� *Type+6Q     5*      $
 Размер��6%   $ * 6N    65   �� *Size+6N   5,      � 5/   
   $��2��6   $��10q�6    50      �� 51      $
��Auto �6#   �� 52      $��* �6#   �� 53      $
��Auto �6#   .+�57      ��  �� Orientation$ 
Horizontal=�6   $��Center=�62   .+�58      �� $��Всего файлов:��6   $��Center=�61   �� 59      -   5        $��TotalFilesTextBlock��59      $	��5,0q�67   $��Center=�6D   �� 5:      $��Выбрано:��6   $��Center=�6,   �� 5;      -   5        $��SelectedFilesTextBlock��5;      $	��5,0q�6:   $��Center=�6G   5<      �� 5?      $��1��6   $ 
Horizontal=�6)   $��Center=�6B   $��Center=�6_   .+�5@      	� -   5        $��ExtractRadioButton��5@      $��Извлечь��68   $��0,0,10,0q�6J   $��Center=�5A   <    d� 	IsChecked$
 TrueY�6W   	� 5B      -   5        $��PackRadioButton��5B      $��Архивировать��65   $��Center=�5C   <   5D      �� 5G      -	   5        $��ExecuteButton��5G      $��2��6*   $��Выполнить��6:   $��20,0,0,0q�6N   $	��100��6`   $��Right=�5H      $��Center=�61   6L   5I      5J      5K      