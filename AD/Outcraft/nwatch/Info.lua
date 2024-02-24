g_PluginInfo =
{
	Name = "NWatch",
	Version = "1.0",
	Date = "2024-01-18",
	Description = [[Control nimda minecraft server]],
	Commands =
	{
		['/nimda'] =
		{
			Permission = "core.help",
			HelpString = "Nimda plugin",
			Handler = nimdaHandler
		}
	}
}
