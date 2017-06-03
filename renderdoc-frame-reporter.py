# https://github.com/vinjn/renderdoc-frame-reporter
# \renderdoc\renderdocui\Code\Core.cs

dump_draws = True
dump_draw_events = True
dump_draw_children = True
dump_frame_stats = False
dump_textures = True
dump_buffers = True

rdc = pyrenderdoc
output_name = rdc.LogFileName + ".draw.md.html"
file = open(output_name,"w") 

file.write("* %s\n" % rdc.LogFileName)
file.write("* API: %s\n" % (rdc.APIProps.pipelineType))

# frameStats
if dump_frame_stats:
	frameStats = rdc.FrameInfo.stats
	file.write("|name|calls|\n")
	file.write("|-|-|\n")

	file.write("|%s|%d|\n" % ("VS", frameStats.draws.calls))

def linkable_ResID(id):
	return "[ResID_%s](#ResID_%s)" % (id, id)

def anchor_ResID(id):
	return "<a name=ResID_%s></a>ResID_%s" % (id, id)

def dump_draw(draw, level):
	if draw.flags & renderdoc.DrawcallFlags.APICalls:
		pass
	if draw.flags & renderdoc.DrawcallFlags.PassBoundary:
		pass

	file.write("%s %s\n" % ("#"*level, draw.name))
	# file.write("`%s`\n" % draw.flags)

	# draw
	if draw.flags & renderdoc.DrawcallFlags.Drawcall:
		file.write("|C0|C1|C2|C3|C4|C5|C6|C7|Z|\n")
		file.write("|-|-|-|-|-|-|-|-|-|\n")
		for output in draw.outputs:
			if output == renderdoc.ResourceId.Null:
				file.write("|null")
			else:
				file.write("|%s" % linkable_ResID(output))
		if draw.depthOut == renderdoc.ResourceId.Null:
			file.write("|null")
		else:
			file.write("|%s" % linkable_ResID(draw.depthOut))

		file.write("|\n")

	# copy
	if draw.flags & renderdoc.DrawcallFlags.Copy:
		file.write("|src|dst|\n")
		file.write("|-|-|\n")
		file.write("|%s|%s|\n" % (linkable_ResID(draw.copySource), linkable_ResID(draw.copyDestination)))

	if dump_draw_events:
		for evt in draw.events:
			desc = evt.eventDesc
			file.write("\n```json\n%s\n```\n" % (desc))
	
	if dump_draw_children:
		for child in draw.children:
			dump_draw(child, level+1)

if dump_draws:
	file.write("# Draws\n")
	for draw in rdc.CurDrawcalls:
		dump_draw(draw, 2)

if dump_textures:
	file.write("# Textures\n")
	file.write("|name|type|format|flags|dim[array]|mips|bytes|MSAA|ID|\n")
	file.write("|:---|:---|:-----|:----|:---------|:---|:----|:---|:-|\n");
	for tex in rdc.CurTextures:
		file.write("|%s|%s|%s|%s|%dx%dx%d[%d]|%d|%d|%d.%d|%s|\n" %
			(tex.name, tex.resType, tex.format, tex.creationFlags,
			tex.width, tex.height, tex.depth, tex.arraysize, tex.mips,
			tex.byteSize, tex.msSamp, tex.msQual,
			anchor_ResID(tex.ID)
		))

if dump_buffers:
	file.write("# Buffers\n")
	file.write("|name|flags|bytes|ID|\n")
	file.write("|:---|:----|:-----|--|\n");
	for buf in rdc.CurBuffers:
		file.write("|%s|%s|%d|%s|\n" %
			(buf.name, buf.creationFlags,buf.length, anchor_ResID(buf.ID)
		))

markdeep_ending = """
<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="markdeep.min.js"></script><script src="https://casual-effects.com/markdeep/latest/markdeep.min.js?"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>
"""

file.write(markdeep_ending)
file.close()

print("%s" % (output_name))
