-- Second-edition EPUB filter.
-- 1. Drop the Markdown title block (everything before the first level-1
--    heading after the book title); the EPUB carries title metadata and a cover.
-- 2. Render backtick-wrapped Scripture inside block quotes as styled text
--    (class "scripture") instead of monospace code.
local function scripture(block)
  return pandoc.walk_block(block, {
    Code = function(c) return pandoc.Span({pandoc.Str(c.text)}, {class = "scripture"}) end
  })
end

function Pandoc(doc)
  local out, seen_title, started = {}, false, false
  for _, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 1 then
      if not seen_title then
        seen_title = true
      else
        started = true
        table.insert(out, b)
      end
    elseif started then
      if b.t == "BlockQuote" then b = scripture(b) end
      table.insert(out, b)
    end
  end
  doc.blocks = out
  return doc
end
