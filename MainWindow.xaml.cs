using System;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Forms;
using Microsoft.Win32;
using IWshRuntimeLibrary;

namespace AndroidSDKInstaller
{
    public partial class MainWindow : Window, INotifyPropertyChanged
    {
        private string installationPath;
        private const string PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip";
        private readonly HttpClient httpClient;

        public event PropertyChangedEventHandler PropertyChanged;

        public string InstallationPath
        {
            get => installationPath;
            set
            {
                installationPath = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(InstallationPath)));
            }
        }

        public MainWindow()
        {
            InitializeComponent();
            DataContext = this;
            httpClient = new HttpClient();
            InstallationPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "Android\\platform-tools");
        }

        private async void InstallButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                InstallButton.IsEnabled = false;
                StatusText.Text = "Downloading platform tools...";

                string tempPath = Path.Combine(Path.GetTempPath(), "platform-tools.zip");
                using (var response = await httpClient.GetAsync(PLATFORM_TOOLS_URL, HttpCompletionOption.ResponseHeadersRead))
                {
                    var totalBytes = response.Content.Headers.ContentLength ?? -1L;
                    using (var fileStream = File.Create(tempPath))
                    using (var downloadStream = await response.Content.ReadAsStreamAsync())
                    {
                        byte[] buffer = new byte[8192];
                        long totalBytesRead = 0;
                        int bytesRead;

                        while ((bytesRead = await downloadStream.ReadAsync(buffer, 0, buffer.Length)) > 0)
                        {
                            await fileStream.WriteAsync(buffer, 0, bytesRead);
                            totalBytesRead += bytesRead;

                            if (totalBytes > 0)
                            {
                                var progress = (double)totalBytesRead / totalBytes;
                                InstallProgress.Value = progress * 100;
                                ProgressText.Text = $"{progress:P0}";
                            }
                        }
                    }
                }

                StatusText.Text = "Extracting files...";
                Directory.CreateDirectory(InstallationPath);
                System.IO.Compression.ZipFile.ExtractToDirectory(tempPath, InstallationPath, true);

                if (AddToPathCheckBox.IsChecked == true)
                {
                    AddToPath();
                }

                if (CreateShortcutCheckBox.IsChecked == true)
                {
                    CreateDesktopShortcut();
                }

                File.Delete(tempPath);
                StatusText.Text = "Installation completed successfully!";
                InstallProgress.Value = 100;
                ProgressText.Text = "100%";

                System.Windows.MessageBox.Show("Android Platform Tools have been successfully installed!", "Installation Complete", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show($"Error during installation: {ex.Message}", "Installation Error", MessageBoxButton.OK, MessageBoxImage.Error);
                StatusText.Text = "Installation failed.";
            }
            finally
            {
                InstallButton.IsEnabled = true;
            }
        }

        private void AddToPath()
        {
            var environmentKey = Registry.LocalMachine.OpenSubKey(@"System\CurrentControlSet\Control\Session Manager\Environment", true);
            var path = (string)environmentKey?.GetValue("Path", "", RegistryValueOptions.DoNotExpandEnvironmentNames);
            if (!path.Contains(InstallationPath))
            {
                path = path.TrimEnd(';') + ";" + InstallationPath;
                environmentKey?.SetValue("Path", path, RegistryValueKind.ExpandString);
            }
        }

        private void CreateDesktopShortcut()
        {
            string desktopPath = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            string shortcutPath = Path.Combine(desktopPath, "Platform Tools.lnk");

            WshShell shell = new WshShell();
            IWshShortcut shortcut = (IWshShortcut)shell.CreateShortcut(shortcutPath);
            shortcut.TargetPath = Path.Combine(InstallationPath, "adb.exe");
            shortcut.WorkingDirectory = InstallationPath;
            shortcut.Description = "Android Platform Tools";
            shortcut.Save();
        }

        private void BrowseButton_Click(object sender, RoutedEventArgs e)
        {
            using (var dialog = new FolderBrowserDialog())
            {
                dialog.Description = "Select Installation Directory";
                dialog.SelectedPath = InstallationPath;

                if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    InstallationPath = dialog.SelectedPath;
                }
            }
        }

        private async void CheckUpdatesButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                CheckUpdatesButton.IsEnabled = false;
                StatusText.Text = "Checking for updates...";

                var response = await httpClient.SendAsync(new HttpRequestMessage(HttpMethod.Head, PLATFORM_TOOLS_URL));
                if (response.IsSuccessStatusCode)
                {
                    System.Windows.MessageBox.Show("Updates are available and will be downloaded during installation.", "Update Check", MessageBoxButton.OK, MessageBoxImage.Information);
                }
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show($"Error checking for updates: {ex.Message}", "Update Check Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                CheckUpdatesButton.IsEnabled = true;
                StatusText.Text = "Ready to install...";
            }
        }
    }
}