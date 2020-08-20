local discordia = require('discordia')


local client = discordia.Client {
	
}
local token = 'NzQ0MDIwMTM3Nzc4MDg1OTU4.XzdIwA.m3QBRGXSWezKhiPc3YFuOTjEVUg'
local prefix = 'pog!'
local class = discordia.class

local mainColor = 0xf54275

local helpFormat = "**"..prefix.."%s** | %s"

local clock = os.clock
function wait(n)  -- seconds
  local t0 = clock()
  while clock() - t0 <= n do end
end

function helpCommand(message, cmds)
	local msg = class.classes.Message
	
	msg['embed'] = {
		fields = {},
		['color'] = mainColor
	}
	
	local field = 1
	
	local desc = ''
	
	for _, cmd in pairs(cmds) do
		
		desc = desc .. "\n" .. string.format(helpFormat, cmd['CMD'], cmd['desc'])
		
	end
	
	msg['embed']['fields'][field] = {}
	msg['embed']['fields'][field]['name'] = 'Commands'
	msg['embed']['fields'][field]['value'] = desc
	msg['embed']['fields'][field]['inline'] = true
	
	message.channel:send(msg)
end

local commands = {
	{CMD = 'help', aliases = {'cmds'}, desc = 'Displays this embed', func = helpCommand}
}

client:on('messageCreate', function(message)
	if string.sub(message.content,1,1) == prefix and not message.author.bot then -- Checks if message is a command
		
		for _, v in pairs(commands) do
			if string.sub(message.content, 2, #message.content) == v['CMD'] then
				v['func'](message, commands)
			else
				for _, alias in pairs(v['aliases']) do
					if string.sub(message.content, 2, #message.content) == alias then
						v['func'](message, commands)
					end
				end
			end
		
		end
		
		
	end
end)

client:on('ready', function()
	print('Logged in as '.. client.user.username)
	local channels = {client:getChannel('739583878020202597'), client:getChannel('739583836467495064')}

	function startPogging(interval)
		while true do
			local channel = channels[math.random(1,#channels)]
			channel:send('pog')
			wait(interval)
		end
	end
	startPogging(60)
	
end)



client:run('Bot '..token)