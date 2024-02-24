function dump(o)
  if type(o) == 'table' then
     local s = '{ '
     for k,v in pairs(o) do
        if type(k) ~= 'number' then k = '"'..k..'"' end
        s = s .. '['..k..'] = ' .. dump(v) .. ','
     end
     return s .. '} '
  else
     return tostring(o)
  end
end

function clanBroadcast(Clan, Message)
  clanUsers = getClanUsers(Clan);

  for i,user in ipairs(clanUsers) do
    cRoot:Get():DoWithPlayerByUUID(user.memberUUID,
    function(User)
      User:SendMessageInfo(Message);
      return true;
    end);
  end
  return true;
end

function clanStaffBroadcast(Clan, Message)
  clanUsers = getClanUsers(Clan);

  for i,user in ipairs(clanUsers) do
    if user.role == 'owner' or user.role == 'moderator' then
      cRoot:Get():DoWithPlayerByUUID(user.memberUUID,
        function(User)
          User:SendMessageInfo(Message);
          return true;
        end);
    end
  end
  return true;
end

function addInvite(FromUser, ToUser)
  local toUserUUID = ToUser:GetUUID();
  local fromUserUUID = FromUser:GetUUID();

  if not storage[toUserUUID] then storage[toUserUUID] = {}; end
  if not storage[toUserUUID]['invintations'] then storage[toUserUUID]['invintations'] = {}; end
  table.insert(storage[toUserUUID]['invintations'], fromUserUUID);

  return true;
end

function addWish(FromUser, ToClan)
  if not storage[ToClan.id] then storage[ToClan.id] = {}; end
  if not storage[ToClan.id]['willing'] then storage[ToClan.id]['willing'] = {}; end
  table.insert(storage[ToClan.id]['willing'], FromUser:GetUUID());

  return true;
end

function isWishExists(FromUser, ToClan)
  if not storage[ToClan.id] then return false; end
  if not storage[ToClan.id]['willing'] then return false; end
  for i, val in ipairs(storage[ToClan.id]['willing']) do
    if val == FromUser:GetUUID() then
      return true;
    end
  end

  return false;
end

function getWishes(Clan)
  if storage[Clan.id] then
    if storage[Clan.id]['willing'] then
      return storage[Clan.id]['willing']
    end
  end
  return {};
end

function clearWishes(Clan)
  if not storage[Clan.id] then storage[Clan.id] = {}; end
  storage[Clan.id]['willing'] = {};
  return true;
end

function removeAllWishesFromUser(FromUser)
  local clans = getClans();
  local uuid = FromUser:GetUUID();

  for i, clan in ipairs(clans) do
      local wishes = getWishes(clan);
      for i, wish in ipairs(wishes) do if wish == uuid then table.remove(storage[clan.id]['willing'], i); end end
  end
  return true;
end

function removeWish(FromUser, ToClan)
  if not storage[ToClan.id] then FromUser:SendMessageFailure('There\'re no any wishes.') end
  if not storage[ToClan.id]['willing'] then FromUser:SendMessageFailure('There\'re no any wishes.') end

  local uuid = FromUser:GetUUID();

  for i,val in ipairs(storage[ToClan.id]['willing']) do
      if val == uuid then
        table.remove(storage[ToClan.id]['willing'], i);
        break;
      end
  end
  return true;
end

function clearInvites(User)
  local uuid = User:GetUUID();

  if not storage[uuid] then storage[uuid] = {}; end
  if not storage[uuid]['invintations'] then storage[uuid]['invintations'] = {}; end

  storage[uuid]['invintations'] = {};

  return true;
end

function getInvites(User)
  local uuid = User:GetUUID();

  if storage[uuid] then
    if storage[uuid]['invintations'] then
      return storage[uuid]['invintations']
    end
  end
  return {};
end

function isInviteExists(User, FromUser)
  local fromUserUUID = FromUser:GetUUID();

  local invites = getInvites(User);
  for i, val in ipairs(invites) do
    if val == fromUserUUID then
      return true;
    end
  end
end

function delInvite(FromUser, ToUser)
  local fromUserUUID = FromUser:GetUUID();
  local toUserUUID = ToUser:GetUUID();

  if storage[toUserUUID]['invintations'] then
    iterator = 1;
    for key, value in ipairs(storage[toUserUUID]['invintations']) do
      if value == fromUserUUID then
        table.remove(storage[toUserUUID]['invintations'], iterator);
        return true
      end
      iterator = iterator + 1;
    end
  end
  return false;
end

function checkCName(Name)
  return string.match(Name, "^[A-Za-z0-9=]+$", 0) ~= nil;
end

function GetPlayerLookPos(Player)
	local World = Player:GetWorld()
	local Start = Player:GetEyePosition()
	local End = Start + Player:GetLookVector() * 150
	local HitCoords = nil
	local Callbacks =
	{
		OnNextBlock = function(BlockPos, BlockType)
			if BlockType ~= E_BLOCK_AIR then
				HitCoords = BlockPos
				return true
			end
		end
	}
	cLineBlockTracer:Trace(World, Callbacks, Start, End)
	return HitCoords
end