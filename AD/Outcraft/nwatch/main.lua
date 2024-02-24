storage = {}

function Initialize(Plugin)
	Plugin:SetName(g_PluginInfo.Name);
	Plugin:SetVersion(g_PluginInfo.Version);

	initDB();
	cPluginManager:AddHook(cPluginManager.HOOK_TAKE_DAMAGE, onDamage);


	dofile(cPluginManager:GetPluginsPath() .. "/InfoReg.lua");
	RegisterPluginInfoCommands();
	RegisterPluginInfoConsoleCommands();

	LOG("Initialised " .. Plugin:GetName() .. " v." .. Plugin:GetVersion())
	return true
end
