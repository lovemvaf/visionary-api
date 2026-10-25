using System;
using System.Windows.Forms;
using Visionary.Desktop.Forms;

namespace Visionary.Desktop;

static class Program
{
    /// <summary>
    /// The main entry point for VISIONARY Club Administration (Desktop).
    /// </summary>
    [STAThread]
    static void Main()
    {
        ApplicationConfiguration.Initialize();
        Application.Run(new LoginForm());
    }    
}