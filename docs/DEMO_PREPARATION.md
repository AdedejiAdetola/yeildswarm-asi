# 🎬 Demo Video Preparation Checklist

**YieldSwarm AI - ASI Alliance Hackathon Submission**

This document provides everything you need to record a professional demo video for your hackathon submission.

---

## 📋 Pre-Recording Setup (30 minutes before)

### ✅ Technical Setup

**1. Verify All Agents Are Running**
```bash
cd /home/grey/web3/yieldswarm-asi

# Check if agents are running
ps aux | grep python | grep agents_agentverse

# If not running, start them
./start_agents.sh

# Wait 30 seconds for all agents to initialize

# Verify agents are responsive
./check_system_status.sh
```

**Expected Output:**
```
✅ Portfolio Coordinator (Port 8000): RUNNING
✅ Chain Scanner (Port 8001): RUNNING
✅ MeTTa Knowledge (Port 8002): RUNNING
✅ Strategy Engine (Port 8003): RUNNING
🚧 Execution Agent (Port 8004): [Optional - in development]
🚧 Performance Tracker (Port 8005): [Optional - in development]
```

**2. Test ASI:One Access**
- [ ] Open ASI:One interface (https://asi1.ai or appropriate URL)
- [ ] Log in to your account
- [ ] Search for "YieldSwarm Portfolio Coordinator"
- [ ] Verify agent appears in search results
- [ ] Open chat with agent
- [ ] Send test message: "Hello"
- [ ] Confirm agent responds within 10 seconds

**3. Prepare Test Queries**

Have these ready to copy-paste during demo:

**Primary Query (for live demo):**
```
I want to invest 10 ETH with moderate risk across Ethereum and Polygon
```

**Backup Queries (if primary fails):**
```
Invest 5 ETH conservatively on Ethereum only
```

```
Show me aggressive yield strategies for 20 ETH across all chains
```

```
What are the best DeFi opportunities with medium risk?
```

**4. Screen Recording Software Setup**

**Mac Users:**
- QuickTime Player (built-in): Open QuickTime → File → New Screen Recording
- ScreenFlow (recommended): Higher quality, easier editing
- OBS Studio (free, powerful): https://obsproject.com/

**Windows Users:**
- Xbox Game Bar (built-in): Win + G
- OBS Studio (free, powerful): https://obsproject.com/
- Camtasia (paid): https://www.techsmith.com/video-editor.html

**Linux Users:**
- SimpleScreenRecorder: sudo apt install simplescreenrecorder
- OBS Studio: https://obsproject.com/
- Kazam: sudo apt install kazam

**Recording Settings:**
- Resolution: 1920x1080 (1080p minimum)
- Frame rate: 30 fps or 60 fps
- Audio: Enable microphone input
- Format: MP4 (H.264 codec preferred)

**5. Audio Setup**
- [ ] Test microphone (record 10 seconds, play back)
- [ ] Check volume levels (speak at normal volume, no clipping)
- [ ] Reduce background noise (close windows, turn off fans if possible)
- [ ] Use headphones while recording (prevents echo)
- [ ] Have water nearby (stay hydrated, avoid dry mouth)

**6. Browser/Desktop Cleanup**
- [ ] Close all unnecessary tabs
- [ ] Close Slack, Discord, email clients
- [ ] Turn off desktop notifications:
  - Mac: System Preferences → Notifications → Do Not Disturb → ON
  - Windows: Settings → System → Focus Assist → Priority only
  - Linux: Settings → Notifications → Do Not Disturb
- [ ] Hide bookmarks bar (cleaner look)
- [ ] Zoom browser to 100% or 110% (for readability)
- [ ] Clear browser history/autocomplete (avoid embarrassment)

**7. Visual Assets Ready**

Prepare these images/slides in advance:

- [ ] YieldSwarm AI logo or title card
- [ ] Architecture diagram showing 4 agents (+ 2 future outlined)
- [ ] ASI Alliance logos (Fetch.ai, SingularityNET, uAgents, MeTTa)
- [ ] Innovation Lab badge: ![Innovation Lab](https://img.shields.io/badge/innovationlab-3D8BD3)
- [ ] Hackathon badge: ![Hackathon](https://img.shields.io/badge/hackathon-5F43F1)
- [ ] End card with GitHub link and agent address
- [ ] Optional: Screenshots of MeTTa code

**Location for visuals:**
```bash
# Create assets folder if needed
mkdir -p /home/grey/web3/yieldswarm-asi/docs/demo_assets

# Store your images here:
# - title_card.png
# - architecture_diagram.png
# - asi_logos.png
# - end_card.png
```

---

## 🎬 Recording Checklist

### Environment Setup (5 minutes before recording)

- [ ] Close all distracting applications
- [ ] Put phone on silent/airplane mode
- [ ] Inform household members you're recording (avoid interruptions)
- [ ] Good lighting (face a window or use desk lamp)
- [ ] Comfortable seating position
- [ ] Glass of water within reach
- [ ] Script/notes printed or on second monitor

### Camera Setup (if recording yourself)

- [ ] Position camera at eye level
- [ ] Check framing (head and shoulders visible)
- [ ] Clean background (or use virtual background if needed)
- [ ] Good lighting on face (not backlit)
- [ ] Test camera focus

### Recording Settings Verified

- [ ] Screen recording enabled
- [ ] Microphone selected and working
- [ ] Audio levels checked (green, not red)
- [ ] Recording area set to full screen or specific window
- [ ] FPS set to 30 or 60
- [ ] File save location has enough space (aim for < 1GB for 3 min video)

---

## 🎤 Recording Process

### Step-by-Step Recording Guide

**1. Start Recording**
- Open screen recording software
- Start recording (usually red button or hotkey)
- Wait 3 seconds before speaking (gives clean edit point)

**2. Scene 1: Title Card (0:00-0:05)**
- Display title card or slide: "YieldSwarm AI"
- Fade to problem visuals
- Begin narration

**3. Scene 2: Problem Statement (0:05-0:20)**
- Show screenshots of DeFi dashboards OR slides with problem stats
- Narrate the problem clearly
- End with transition text: "Enter YieldSwarm AI"

**4. Scene 3: Solution Overview (0:20-0:50)**
- Display slide with 4 solid agents + 2 outlined future agents
- Show ASI Alliance logos
- Narrate agent capabilities
- Emphasize "built on ASI Alliance stack"

**5. Scene 4: Live Demo (0:50-1:50)** ⭐ **MOST CRITICAL**
- Switch to ASI:One interface
- Screen should be visible and clear
- Type or paste test query
- Point with mouse cursor at key information as it appears
- Narrate what's happening in real-time
- Allow natural pauses for agent processing (5-10 seconds)
- Highlight the response sections

**Tips for Live Demo:**
- If agent is slow, narrate what it's doing ("the agents are coordinating...")
- If agent fails, stay calm, use backup query
- Zoom browser to 110-120% if text is small
- Use mouse cursor to point at important info
- Speak slowly and clearly

**6. Scene 5: Technical Deep Dive (1:50-2:20)**
- Display architecture diagram
- Quick cut to Agentverse dashboard (show 4 agents)
- Show MeTTa code snippet (optional)
- Narrate technical highlights

**7. Scene 6: Impact & CTA (2:20-2:40)**
- Display stats overlay
- Show GitHub repository page
- Display end card with:
  - Agent address
  - GitHub link
  - "Try on ASI:One" call-to-action
  - Innovation Lab + Hackathon badges
- Thank viewers

**8. Stop Recording**
- Pause for 3 seconds after final words
- Stop recording
- Save file immediately

---

## 🎬 During Recording - Quick Reference

### What to Say (Abbreviated Script)

**[0:00-0:20] Problem:**
> "DeFi investors face an impossible challenge... losing 15-30% returns... $20B market problem."

**[0:20-0:50] Solution:**
> "YieldSwarm AI - autonomous multi-agent system. Four live agents: Coordinator, Scanner, MeTTa Knowledge, Strategy Engine. Two more in development. Built on ASI Alliance stack."

**[0:50-1:50] Demo:**
> "Let's see it in action. [Type query]. Watch the coordination: Scanner fetches data, MeTTa reasons through 22 protocols, Strategy Engine optimizes. Explainable AI."

**[1:50-2:20] Technical:**
> "First MeTTa-powered DeFi optimizer. Four live agents on uAgents framework. Natural language via ASI:One. Perfect ASI Alliance vision."

**[2:20-2:40] Impact:**
> "Four agents live on Agentverse. 22 protocols, 5 chains, 54+ tests. Try it on ASI:One. GitHub link. Future of DeFi. Thank you!"

### Voice & Delivery Tips

✅ **Do:**
- Smile while speaking (sounds friendlier)
- Vary your tone (enthusiastic, serious, professional)
- Pause naturally between sections
- Enunciate clearly
- Sound confident

❌ **Don't:**
- Rush (speak slower than you think you should)
- Use filler words ("um", "uh", "like", "so")
- Apologize or sound uncertain
- Read word-for-word robotically
- Speak in monotone

---

## ⚠️ Common Issues & Solutions

### Issue 1: Agent Not Responding on ASI:One

**Solutions:**
1. Wait 30 seconds (agents may be initializing)
2. Refresh ASI:One page
3. Check local agents are running: `./check_system_status.sh`
4. Restart agents: `./stop_agents.sh && ./start_agents.sh`
5. Use backup pre-recorded demo footage

**Prevention:**
- Test 10 minutes before recording
- Have backup recording ready
- Keep agents running continuously before demo

### Issue 2: Poor Audio Quality

**Solutions:**
1. Move closer to microphone (6-12 inches away)
2. Reduce background noise (close windows, turn off AC)
3. Use a better microphone (USB mic recommended)
4. Record in small, quiet room (less echo)
5. Use noise reduction in post-production

**Prevention:**
- Test audio 5 minutes before
- Record in quiet environment
- Use headphones to monitor

### Issue 3: Screen Recording Lag

**Solutions:**
1. Close other applications
2. Reduce recording resolution to 720p
3. Reduce frame rate to 30 fps
4. Free up disk space
5. Restart computer before recording

**Prevention:**
- Test recording beforehand
- Ensure sufficient RAM/CPU available
- Use external SSD for recording storage

### Issue 4: Forgot Important Point

**Solutions:**
1. Don't stop - continue recording
2. Re-record specific scene later
3. Edit in post-production
4. Add text overlay in editing

**Prevention:**
- Practice 2-3 times before final recording
- Have script visible
- Record in small sections if needed

### Issue 5: Made a Mistake While Speaking

**Solutions:**
1. Pause for 3 seconds
2. Start sentence again
3. Continue recording
4. Cut out mistake in editing

**Prevention:**
- Practice beforehand
- Don't aim for perfection
- Plan to edit

---

## 🎨 Post-Production Checklist

### Editing Tasks

**1. Import Footage**
- [ ] Import video file into editor (iMovie, DaVinci Resolve, Premiere, etc.)
- [ ] Import audio separately if recorded separately
- [ ] Import visual assets (title cards, diagrams, end card)

**2. Video Editing**
- [ ] Cut dead air at beginning and end
- [ ] Remove any mistakes or long pauses
- [ ] Trim to 2:30 - 3:00 minutes total
- [ ] Add title card at start (3-5 seconds)
- [ ] Add end card at end (8-10 seconds)
- [ ] Insert architecture diagram in technical section
- [ ] Add smooth transitions between scenes (optional)

**3. Audio Editing**
- [ ] Remove background noise (use noise reduction filter)
- [ ] Normalize audio levels (-3dB to -1dB peak)
- [ ] Remove clicks, pops, breath sounds (optional)
- [ ] Add subtle background music (20-30% volume)
  - Use royalty-free music only
  - Fade in at start, fade out at end
  - Lower volume during narration

**4. Text Overlays (Optional but Professional)**
- [ ] Section titles: "The Problem", "The Solution", "Live Demo", "Technical Architecture", "Try It Now"
- [ ] Key stats as text: "22 Protocols", "5 Blockchains", "4 Live Agents"
- [ ] Agent names when first mentioned
- [ ] Highlight important quotes or features

**5. Branding**
- [ ] Add YieldSwarm AI logo/title (first 3 seconds)
- [ ] Add ASI Alliance logo watermark (bottom corner, subtle, throughout)
- [ ] Add Innovation Lab + Hackathon badges on end card

**6. Color Correction (if needed)**
- [ ] Adjust brightness if too dark
- [ ] Adjust contrast for clarity
- [ ] Ensure text is readable

**7. Final Checks**
- [ ] Watch entire video from start to finish
- [ ] Check audio sync with video
- [ ] Verify all text is readable
- [ ] Ensure smooth flow between sections
- [ ] Confirm duration is 2:30 - 3:00 minutes (within hackathon guidelines)

### Export Settings

**Recommended Export Settings:**
- **Format:** MP4
- **Codec:** H.264
- **Resolution:** 1920x1080 (1080p) or 3840x2160 (4K)
- **Frame Rate:** 30 fps or 60 fps (match recording)
- **Bitrate:** 8-12 Mbps (good quality, reasonable file size)
- **Audio:** AAC, 192 kbps, 48 kHz
- **Target File Size:** Under 500 MB (easier to upload)

**Export Checklist:**
- [ ] File format: MP4
- [ ] Resolution: 1080p minimum
- [ ] Duration: 2:30 - 3:00 minutes
- [ ] Audio: Clear and loud enough
- [ ] File size: Under 500 MB
- [ ] Video plays on all devices (test on phone, computer)

---

## 📤 Upload & Submission Checklist

### YouTube Upload (Recommended Platform)

**1. Prepare Video File**
- [ ] Final edited video (MP4)
- [ ] File size under 500 MB (or compress if needed)

**2. Upload to YouTube**
- [ ] Go to https://youtube.com/upload
- [ ] Upload video file
- [ ] Wait for processing (may take 5-30 minutes)

**3. Video Details**
```
Title: YieldSwarm AI - ASI Alliance Hackathon Submission | Multi-Agent DeFi Yield Optimizer

Description:
YieldSwarm AI is an autonomous multi-agent DeFi yield optimizer built on the ASI Alliance technology stack. Four specialized AI agents coordinate to provide intelligent investment strategies across 5 blockchains and 22 DeFi protocols.

🤖 Four Live Agents:
• Portfolio Coordinator (ASI:One Chat Protocol)
• Chain Scanner (5 blockchains, 20+ protocols)
• MeTTa Knowledge Agent (22-protocol symbolic AI)
• Strategy Engine (risk-adjusted optimization)

🔮 In Development:
• Execution Agent
• Performance Tracker

🔗 Links:
• GitHub: [Your GitHub URL]
• Try on ASI:One: Search "YieldSwarm Portfolio Coordinator"
• Agent Address: agent1qwumkwejd0rxnxxu64yrl7vj3f29ydvvq85yntvrvjyzpce86unwxhfdz5a

🏆 Built with ASI Alliance Stack:
✅ Fetch.ai uAgents Framework
✅ SingularityNET MeTTa / OpenCog Hyperon
✅ Agentverse Registry
✅ ASI:One Chat Protocol

#ASIAlliance #Hackathon #DeFi #FetchAI #MeTTa #uAgents #Web3 #AI

Tags (YouTube): asi-alliance, hackathon, fetch-ai, metta, defi, blockchain, web3, uagents, artificial-intelligence, cryptocurrency, yield-farming, multi-agent-system
```

**4. Thumbnail**
- [ ] Create custom thumbnail (1280x720 pixels)
- [ ] Include YieldSwarm branding
- [ ] Add text: "4 AI Agents", "Live Demo", "ASI Alliance"
- [ ] Use high contrast colors
- [ ] Make it eye-catching

**5. Upload Settings**
- [ ] Visibility: **Public** or **Unlisted** (Public recommended for hackathon)
- [ ] Playlist: Create "ASI Alliance Hackathon" playlist
- [ ] Category: Science & Technology
- [ ] Allow comments: Yes
- [ ] Allow embedding: Yes

**6. Verify Upload**
- [ ] Video plays correctly
- [ ] Audio is synchronized
- [ ] Title and description are correct
- [ ] Thumbnail looks good
- [ ] Quality is 1080p or higher

### Hackathon Submission

**1. Copy Video Link**
```
Example: https://youtube.com/watch?v=YOUR_VIDEO_ID
```

**2. Add to Hackathon Submission Form**
- [ ] Paste YouTube link in "Demo Video" field
- [ ] Verify link works (open in incognito/private browser)
- [ ] Ensure video is publicly accessible

**3. Add to GitHub README**
- [ ] Update README.md with video link
- [ ] Add "Demo Video" section near top
- [ ] Embed video or add clickable link

**4. Final Hackathon Submission Checklist**
- [ ] ✅ Code in public GitHub repository
- [ ] ✅ README.md with agent addresses
- [ ] ✅ Innovation Lab badge in README
- [ ] ✅ Hackathon badge in README
- [ ] ✅ Demo video (3-5 minutes) uploaded and linked
- [ ] ✅ All 4 agents live on Agentverse
- [ ] ✅ Chat Protocol enabled (ASI:One compatible)
- [ ] ✅ Comprehensive documentation

---

## 🎯 Quality Standards

### What Makes a Great Demo Video

**Technical Quality:**
✅ 1080p resolution minimum
✅ Clear audio (no background noise)
✅ Smooth transitions
✅ Professional looking (clean, organized)
✅ Proper lighting and framing

**Content Quality:**
✅ Starts with strong hook (first 10 seconds)
✅ Clearly explains the problem
✅ Shows actual working system (not just slides)
✅ Demonstrates all key features
✅ Explains technical innovation
✅ Provides clear call-to-action
✅ Stays within time limit (2:30-3:00 mins ideal)

**Presentation Quality:**
✅ Confident narration
✅ Good pacing (not too fast/slow)
✅ Clear pronunciation
✅ Engaging energy
✅ Professional tone

### Common Mistakes to Avoid

❌ **Content Mistakes:**
- Too much theory, not enough demo
- No live demonstration
- Video too long (over 5 minutes)
- Video too short (under 2 minutes)
- Unclear value proposition
- No call-to-action

❌ **Technical Mistakes:**
- Poor audio quality
- Low resolution (below 720p)
- Screen too small to read
- Audio out of sync
- Video lags or stutters

❌ **Presentation Mistakes:**
- Speaking too fast
- Monotone voice
- Reading word-for-word
- Too many "um"s and "uh"s
- Apologizing or sounding uncertain

---

## 🚀 Final Pre-Submit Checklist

**24 Hours Before Submission:**
- [ ] Video fully edited and exported
- [ ] Uploaded to YouTube
- [ ] Thumbnail created and uploaded
- [ ] Title and description finalized
- [ ] Video tested on multiple devices
- [ ] Link added to GitHub README
- [ ] All hackathon requirements met

**1 Hour Before Submission:**
- [ ] Watch video one final time
- [ ] Verify YouTube link works
- [ ] Check GitHub README displays correctly
- [ ] Ensure all agents are running on Agentverse
- [ ] Test ASI:One chat one more time

**At Submission Time:**
- [ ] Submit hackathon form with video link
- [ ] Double-check all fields are filled
- [ ] Save confirmation email/screenshot
- [ ] Celebrate! 🎉

---

## 📞 Emergency Contacts & Resources

### If Something Goes Wrong

**ASI Alliance Support:**
- Discord: https://discord.gg/fetch-ai (or appropriate link)
- Documentation: https://innovationlab.fetch.ai/resources/docs
- MeTTa Docs: https://metta-lang.dev/docs

**Screen Recording Issues:**
- OBS Studio Guide: https://obsproject.com/wiki/
- QuickTime Help: https://support.apple.com/guide/quicktime-player/

**Video Editing Help:**
- DaVinci Resolve Tutorials: https://www.blackmagicdesign.com/products/davinciresolve/training
- iMovie Help: https://support.apple.com/imovie

### Backup Plan

**If Live Demo Completely Fails:**
1. Use backup pre-recorded footage
2. Or demonstrate locally with terminal/agent logs
3. Or walk through code and architecture with screenshots
4. Still submit - show what you built even if demo isn't perfect

**Remember:** Judges want to see working systems, but they understand technical demos can be unpredictable. Show your best effort, explain clearly, and demonstrate the value you've built.

---

## ✅ Final Words

**You've built something impressive. Now show the world!**

**Key Principles:**
1. **Preparation is everything** - Test thoroughly before recording
2. **Practice makes perfect** - Rehearse 2-3 times
3. **Show, don't just tell** - Live demo beats slides
4. **Be authentic** - Your passion for the project will shine through
5. **Have fun!** - This is your moment to showcase your hard work

**Good luck! You've got this! 🚀**

---

**YieldSwarm AI Team**
*Built with ❤️ using the ASI Alliance Technology Stack*
