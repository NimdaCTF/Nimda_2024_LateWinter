using System;
using System.Net.Http;
using System.Text;
using System.Windows;


namespace FirstJustice
{
    public partial class MainWindow : Window
    {
        private readonly HttpClient _client;

        public MainWindow()
        {
            InitializeComponent();

            _client = new HttpClient();
            _client.BaseAddress = new Uri(Properties.Settings.Default.ApiUrl);
        }

        private async void Button_Click(object sender, RoutedEventArgs e)
        {
            var jsonBody = "{\"login\":\"" + tbxLogin.Text + "\",\"password\":\"" + tbxPassword.Password + "\", \"key\": \""+ TokenGenerator.TokenGenerator.GetToken() +"\"}";
            var content = new StringContent(jsonBody, Encoding.UTF8, "application/json");

            try
            {
                var response = await _client.PostAsync("login", content);
                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    if (responseContent == "Ok")
                    {
                        new Flag().Show();
                        this.Close();
                    }
                    else
                    {
                        MessageBox.Show("Eh", "No :D", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
                else
                {
                    MessageBox.Show("Eh", "No :D", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void tbxLogin_GotFocus(object sender, RoutedEventArgs e)
        {
            if (tbxLogin.Text == "Login")
            {
                tbxLogin.Text = string.Empty;
            }
        }

        private void tbxLogin_LostFocus(object sender, RoutedEventArgs e)
        {
            if (tbxLogin.Text == string.Empty)
            {
                tbxLogin.Text = "Login";
            }
        }

        private void tbxPassword_GotFocus(object sender, RoutedEventArgs e)
        {
            if (tbxPassword.Password == "Password")
            {
                tbxPassword.Password = string.Empty;
            }
        }

        private void tbxPassword_LostFocus(object sender, RoutedEventArgs e)
        {
            if (tbxPassword.Password == string.Empty)
            {
                tbxPassword.Password = "Password";
            }
        }
    }
}
