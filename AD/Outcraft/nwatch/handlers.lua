function nimdaHandler(Cmd, User)
  if Cmd[1] == '/nimda' then
    if Cmd[2] then
      if Cmd[2] == 'note' then
        if not Cmd[3] then
          User:SendMessageInfo("Nimda notes is the best way to save ur knowleges");
        else
          if Cmd[3] == 'add' then
            if not Cmd[4] or not Cmd[5] then
              User:SendMessageFailure('Usage: /nimda note add <TEXT> <IS_PRIVATE(1 or 0)>');
              return true;
            end
            if not addNote(User, Cmd[4], Cmd[5]) then
              User:SendMessageFailure('Something went wrong');
              return true;
            end
            User:SendMessageSuccess('Successfully added')
          elseif Cmd[3] == 'get' then
            if not Cmd[4] then
              User:SendMessageFailure('Usage: /nimda note get <TEXT>');
              return true;
            end
            local res = getNote(User, Cmd[4]);
            if res == {} then
              User:SendMessageFailure('Nothing found');
            else
              User:SendMessageInfo(res.value);
            end
          end
        end      
      elseif Cmd[2] == 'light' then
        User:SendMessageFailure('Not implemented yet');
      elseif Cmd[2] == 'hat' then
        changeHat(User);
      elseif Cmd[2] == 'fb' then
        createFireball(User);
      elseif Cmd[2] == 'l' then
        lightingStrike(User);
      elseif Cmd[2] == 'help' then
        generateHelp(User, Cmd[3]);
      else
        User:SendMessageFailure('Command not found');
      end
    else
      User:SendMessageInfo("Usage: /nimda help <page>");
    end
  end
  return true;
end

function generateHelp(User, Page)
  local totalPages = 1;

  if not Page then
    Page = "1";
  end

  if Page == "1" then
    msg =        '\n/nimda - Show usage\n';
    msg = msg .. '/nimda l - Lighting strike\n';
    msg = msg .. '/nimda hat - Set new hat\n';
    msg = msg .. '/nimda fb - Fireball\n';
    -- msg = msg .. '/nimda note - Notes\n'; -- Not ready yet
  else
    User:SendMessageFailure('Invalid page. There\'re ' .. tostring(totalPages) .. ' pages in help.')
    return true;
  end

  msg = msg .. 'Page ' .. Page .. ' of ' .. tostring(totalPages);
  User:SendMessageInfo(msg);
  return true;
end

function addNote(User, note, private)
  if private == '1' then
    private = 1
  elseif private == '0' then
    private = 0
  else 
    User:SendMessageFailure('Private must be 1 or 0');
    return;
  end
  return addNoteDB(note, private, User:GetUUID());
end

function getNote(User, value)
  return getNoteByValueDB(value, User:GetUUID());
end

function changeHat(Player)
	local Hat = cItem(Player:GetEquippedItem())
	Hat.m_ItemCount = 1
	local ArmorSlot = Player:GetInventory():GetArmorSlot(0)
	if not ArmorSlot:IsEmpty() then
		Player:GetInventory():AddItem(ArmorSlot)
	end
	--Set chestplate slot to the item the player is holding
	if not Player:GetEquippedItem():IsEmpty() then
		Player:GetInventory():SetArmorSlot(0, Hat)
		Player:GetInventory():RemoveOneEquippedItem()
		Player:SendMessageSuccess("Enjoy your new hat!")
	else
		Player:SendMessageFailure("Please hold an item")
	end
	return true
end

function createFireball(Player)
	local World = Player:GetWorld()
	local X = Player:GetPosX()
	local Y = Player:GetPosY() + 1.5
	local Z = Player:GetPosZ()
	local Speed = Player:GetLookVector() * 30
	World:CreateProjectile(X, Y, Z, cProjectileEntity.pkGhastFireball, Player, Player:GetEquippedItem(), Speed)
	return true
end

function lightingStrike(Player)
	local LookPos = GetPlayerLookPos(Player)
	Player:GetWorld():CastThunderbolt(Vector3i(LookPos.x, LookPos.y, LookPos.z))
	return true
end
