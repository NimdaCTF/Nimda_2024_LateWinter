using System.IO;
using System.Windows;
using FirstJustice.Utils;

namespace FirstJustice
{
    /// <summary>
    /// Логика взаимодействия для Flag.xaml
    /// </summary>
    public partial class Flag : Window
    {
        public Flag()
        {
            InitializeComponent();
            _init();
        }

        private void _init()
        {
            var userId = DataDep.Data.UserId;
            tbxFlag.Text = Utils.Utils.GetFlag(userId, Properties.Settings.Default.Prefix, Properties.Settings.Default.Secret, Properties.Settings.Default.SaltSize);
            cntMusic.Play();
        }
    }
}
