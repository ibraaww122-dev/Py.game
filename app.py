import streamlit as st

st.set_page_config(page_title="NINJA H2R - For Cona", layout="wide", initial_sidebar_state="collapsed")

# Hilangin header streamlit biar full game
st.markdown("""
<style>
[data-testid="stHeader"]{display:none}
[data-testid="stToolbar"]{display:none}
.block-container{padding:0 !important;margin:0 !important;max-width:100% !important}
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  *{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  body{background:#050514;color:#fff;font-family:Arial;overflow:hidden;height:100vh;display:flex;justify-content:center}
  #wrap{width:100%;max-width:420px;height:100vh;position:relative;overflow:hidden;background:linear-gradient(#0a0a2e,#050514)}
  canvas{width:100%;height:100%;display:block}
  #hud{position:absolute;top:0;left:0;right:0;padding:12px;display:flex;justify-content:space-between;font-weight:900;text-shadow:0 0 10px #0ff;z-index:5;pointer-events:none}
  #title{position:absolute;top:35%;left:0;right:0;text-align:center;z-index:10}
  #title h1{font-size:28px;color:#00ff9d;text-shadow:0 0 20px #00ff9d}
  #title p{margin:8px 0;color:#ccc;font-size:14px}
  #start{padding:14px 30px;font-size:18px;font-weight:900;border:none;border-radius:30px;background:#00ff9d;color:#000}
  #over{position:absolute;inset:0;display:none;align-items:center;justify-content:center;flex-direction:column;background:rgba(0,0,0,.85);z-index:20;text-align:center;padding:20px}
  #over h2{font-size:30px;color:#ff2d78}
  #again{margin-top:15px;padding:12px 25px;border:none;border-radius:25px;background:#fff;font-weight:900}
  .btn{position:absolute;bottom:18px;width:70px;height:70px;border-radius:50%;background:rgba(255,255,255,.15);border:2px solid rgba(255,255,255,.4);color:#fff;font-size:28px;z-index:10}
  #left{left:15px} #right{right:15px}
</style>
</head>
<body>
<div id="wrap">
  <div id="hud"><div>SCORE: <span id="score">0</span></div><div>FOR CONA 🤍</div><div>SPEED: <span id="speed">120</span></div></div>
  <canvas id="game" width="420" height="800"></canvas>
  <div id="title"><h1>🏍️ NINJA H2R<br>NEON RACER</h1><p>Buat Cona, biar lututnya cepet sembuh<br>Swipe / Tap ◀ ▶ buat pindah jalur<br>Ambil ⚡ buat BOOST!</p><button id="start">▶ START RIDE</button></div>
  <button class="btn" id="left">◀</button>
  <button class="btn" id="right">▶</button>
  <div id="over"><h2>CRASH! 💥</h2><p id="final" style="margin:10px"></p><p>Cona bilang: Coba lagi, sayang 🥺</p><button id="again">MAIN LAGI</button></div>
</div>
<script>
const cv=document.getElementById('game'),ctx=cv.getContext('2d');
let lane=1, lanes=[70,210,350], score=0, speed=120, playing=false, traffic=[], boosts=[], roadY=0, boostTime=0, lastSpawn=0;
const playerY=650;
function reset(){ score=0; speed=120; traffic=[]; boosts=[]; lane=1; }
function drawRoad(){
  ctx.fillStyle='#0d0d2a'; ctx.fillRect(0,0,420,800);
  ctx.fillStyle='#00ff9d'; ctx.fillRect(10,0,6,800); ctx.fillRect(404,0,6,800);
  ctx.fillStyle='rgba(0,255,255,.5)';
  for(let y=-80+roadY%80; y<800; y+=80){ ctx.fillRect(140,y,3,40); ctx.fillRect(280,y,3,40); }
}
function drawPlayer(){
  ctx.save(); ctx.translate(lanes[lane],playerY);
  if(boostTime>0){ ctx.shadowColor='#00ff9d'; ctx.shadowBlur=30; }
  ctx.font='64px Arial'; ctx.textAlign='center'; ctx.fillText('🏍️',0,25);
  ctx.font='bold 13px Arial'; ctx.fillStyle='#00ff9d'; ctx.fillText('H2R • CONA',0,50);
  ctx.restore();
}
function loop(t){
  if(!playing) return;
  roadY+= speed/10 + (boostTime>0?8:0);
  if(boostTime>0) boostTime--;
  if(t-lastSpawn>700){ lastSpawn=t; let l=Math.floor(Math.random()*3); traffic.push({lane:l,y:-80,type:Math.random()>0.5?'🚗':'🚙'}); if(Math.random()<0.25) boosts.push({lane:Math.floor(Math.random()*3),y:-150}); }
  drawRoad();
  boosts.forEach((b,i)=>{ b.y+= speed/10; ctx.font='30px Arial'; ctx.textAlign='center'; ctx.fillText('⚡',lanes[b.lane],b.y); if(Math.abs(b.y-playerY)<40 && b.lane==lane){ boostTime=120; score+=20; boosts.splice(i,1);} if(b.y>820) boosts.splice(i,1); });
  traffic.forEach((car,i)=>{
    car.y+= speed/10;
    ctx.font='52px Arial'; ctx.textAlign='center'; ctx.fillText(car.type,lanes[car.lane],car.y);
    if(Math.abs(car.y-playerY)<50 && car.lane==lane){ gameOver(); }
    if(car.y>820){ traffic.splice(i,1); score+=10; speed=Math.min(280,speed+1); }
  });
  drawPlayer();
  document.getElementById('score').innerText=score;
  document.getElementById('speed').innerText= boostTime>0 ? speed*2 : speed;
  if(boostTime>0){ ctx.font='bold 20px Arial'; ctx.fillStyle='#ffff00'; ctx.textAlign='center'; ctx.fillText('BOOST x2 ⚡',210,120); }
  requestAnimationFrame(loop);
}
function gameOver(){
  playing=false;
  document.getElementById('final').innerText='Skor kamu: '+score+' | Buat Cona nih!';
  document.getElementById('over').style.display='flex';
}
function start(){ reset(); document.getElementById('title').style.display='none'; document.getElementById('over').style.display='none'; playing=true; requestAnimationFrame(loop); }
document.getElementById('start').onclick=start;
document.getElementById('again').onclick=start;
document.getElementById('left').onclick=()=>{ if(lane>0) lane--; };
document.getElementById('right').onclick=()=>{ if(lane<2) lane++; };
let sx=0;
cv.addEventListener('touchstart',e=>sx=e.touches[0].clientX);
cv.addEventListener('touchend',e=>{ let dx=e.changedTouches[0].clientX-sx; if(dx<-30 && lane>0) lane--; if(dx>30 && lane<2) lane++; });
document.addEventListener('keydown',e=>{ if(e.key=='ArrowLeft'&&lane>0) lane--; if(e.key=='ArrowRight'&&lane<2) lane++; });
</script>
</body>
</html>
"""

st.components.v1.html(html_code, height=850, scrolling=False)
