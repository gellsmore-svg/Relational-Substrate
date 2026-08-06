local function text(value)
  return pandoc.utils.stringify(value or {})
end

function Pandoc(document)
  local blocks = {}
  local title_removed = false
  local skipping_manual_contents = false
  local remove_manual_contents =
    text(document.meta["epub-remove-manual-contents"]) == "true"

  document.meta["epub-remove-manual-contents"] = nil

  for _, block in ipairs(document.blocks) do
    if not title_removed and block.t == "Header" and block.level == 1 then
      title_removed = true
    elseif skipping_manual_contents then
      if block.t == "Header" and block.level == 1 then
        skipping_manual_contents = false
        table.insert(blocks, block)
      end
    elseif remove_manual_contents
        and block.t == "Header"
        and block.level == 2
        and text(block.content) == "Contents" then
      skipping_manual_contents = true
    else
      table.insert(blocks, block)
    end
  end

  document.blocks = blocks
  return document
end
