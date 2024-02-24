function onDamage(User, TDI)
  if not User:IsPlayer() or not TDI.Attacker:IsPlayer() then
    return false;
  end

  if not User:HasPermission("cclans.disable_friendly_fire") then
      return false;
  end

  local victim = getUser(User);

  if not isUserInClan(User) then
    return false;
  end

  local attacker = tolua.cast(TDI.Attacker, "cPlayer");

  if not isUserInClan(attacker) then
    return false;
  end

  local victimClan = getClan(nil, victim.clanID);

  if isMemberOf(attacker, victimClan) then
    attacker:SendMessageInfo('You can\'t attack your clanmate');
    return true;
  end

  return false;
end
