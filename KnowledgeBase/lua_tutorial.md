```lua

--[[
LUA Tutorials

Just enough lua so that I can customize the Nvim according to myself.
--]]

-- to comment a line
--[[ 
    Adding double square brackets makes it a multi line comment
--]]

NUM = 42
num = 60
somevariable = "Something"  --can also use single quotes, immutable type like python
multiline_string = [[
    Multi
    line
    string
]]

NUM = nil -- undefines num variable, lua has garbage collector


-- blocks are denotes with keywords like do and end
while NUM > 10 do
    NUM = NUM - 10    -- No += or ++ type operator
end

-- If clauses:
if num > 40 then
  print('over 40')
elseif somevariable ~= 'walternate' then  -- ~= is 'not equals'.
  -- Equality check is == like Python; ok for strs.
  io.write('not over 40\n')  -- Defaults to stdout.
else
  -- Variables are global by default.
  thisIsGlobal = 5  -- Camel case is common.

  -- How to make a variable local:
  local line = io.read()  -- Reads next stdin line.

  -- String concatenation uses the .. operator:
  print('Winter is coming, ' .. line)
end

-- Undefined variables return nil.
-- This is not an error:
foo = anUnknownVariable  -- Now foo = nil.

```
