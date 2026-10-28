/* DEHR Ltd — вакансии, фильтры, карта, согласие на аналитику. Данные приходят из window.DEHR (собирает build.py). */
(function(){
'use strict';
var D=window.DEHR||{}, T=D.t||{}, lang=D.lang||'ru', rtl=lang==='he';
var JOBS=D.jobs||[], CITIES=D.cities||{};
var filter='all', city=null;
var $=function(id){return document.getElementById(id)};
var esc=function(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})};
var money=function(n){return Number(n).toLocaleString(lang==='he'?'he-IL':lang==='en'?'en-US':'ru-RU').replace(/ /g,' ')};
var byCat=function(j){return filter==='all'||(filter==='house'?!!j.house:j.cat===filter)};
var inCity=function(j){return !city||j.cities.indexOf(city)>-1};
var cityNames=function(j){return j.cities.map(function(k){return (CITIES[k]||{}).name||k}).join(', ')};
var waLink=function(text){return 'https://wa.me/'+D.wa+'?text='+encodeURIComponent(text)};

var ICON_WA='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.4 14.1c-.2.6-1.3 1.2-1.8 1.3-.5 0-1 .2-3.3-.7-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.3.1.2.1.7-.1 1.3Z"/></svg>';
var ICON_TG='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.5 4.3 2.9 11.5c-1.3.5-1.2 1.2-.2 1.5l4.8 1.5 1.8 5.6c.2.6.4.8.9.8.4 0 .6-.2.9-.5l2.4-2.3 4.9 3.6c.9.5 1.5.2 1.8-.8l3.2-15.1c.3-1.3-.5-1.9-1.4-1.5ZM9.3 14.3l9-5.7c.4-.3.8-.1.5.2l-7.4 6.7-.3 3.3-1.8-4.5Z"/></svg>';
var ICONS={
  fac:'<path d="M3 20V10l5 3V10l5 3V6h4l1 14z"/><path d="M7 17h2M12 17h2"/>',
  food:'<path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M16 21V3c-2 1-3 4-3 8h3"/>',
  clean:'<path d="M9 3h5v3H9zM10 6v3M8 9h7l1 12H7z"/><path d="M14 4h4l1 2"/>',
  auto:'<path d="M3 14l2-5h14l2 5v4H3z"/><circle cx="7.5" cy="18" r="1.5"/><circle cx="16.5" cy="18" r="1.5"/><path d="M3 14h18"/>',
  build:'<path d="M4 16a8 8 0 0 1 16 0"/><path d="M3 16h18v3H3zM12 8V5M10 5h4"/>',
  wh:'<path d="M4 20V9l8-5 8 5v11"/><path d="M8 20v-6h8v6M8 17h8"/>'
};
var cover=function(j){
  return j.photo
    ?'<img class="job-cover" src="/'+esc(j.photo)+'" alt="" loading="lazy" decoding="async" width="1000" height="600">'
    :'<div class="job-cover c-'+esc(j.cat)+'"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true">'+(ICONS[j.cat]||'')+'</svg><span>'+esc((T._cat||{})[j.cat]||'')+'</span></div>';
};

/* ---------- вакансии ---------- */
function renderJobs(){
  var list=$('jobList'); if(!list)return;
  var items=JOBS.filter(function(j){return byCat(j)&&inCity(j)});
  list.innerHTML=items.length?items.map(function(j){
    var msg=(T.wa_job||'').replace('{id}',j.id).replace('{title}',j.title).replace('{cities}',cityNames(j));
    var req='<dt>'+esc(T._who)+'</dt><dd>'+esc(j.who==='m'?T._m:T._all)+'</dd>'+
            '<dt>'+esc(T._docs)+'</dt><dd>'+esc(j.docs||'—')+'</dd>'+
            (j.langs?'<dt>'+esc(T._lang)+'</dt><dd>'+esc(j.langs)+'</dd>':'');
    return '<article class="job" id="job-'+esc(j.id)+'">'+cover(j)+
      '<div class="job-top"><span class="pin">'+esc(cityNames(j))+'</span><code>'+esc(j.id)+'</code></div>'+
      '<h3>'+esc(j.title)+'</h3>'+
      '<div class="rate">'+money(j.pay.amount)+'<small>'+esc(j.pay.per==='month'?T._month:T._hour)+'</small></div>'+
      '<p class="desc">'+esc(j.desc)+'</p>'+
      '<div class="tags">'+(j.tags||[]).map(function(t,k){return '<span class="'+(k===0&&j.house?'house':'')+'">'+esc(t)+'</span>'}).join('')+'</div>'+
      '<dl class="req">'+req+'</dl>'+
      '<div class="job-foot"><a class="btn btn-ink" href="'+esc(waLink(msg))+'" target="_blank" rel="noopener">'+ICON_WA+'<span>'+esc(T._apply)+'</span></a>'+
      '<a class="tg" href="https://t.me/'+esc(D.tg)+'" target="_blank" rel="noopener" aria-label="'+esc(T._apply_tg)+'" title="'+esc(T._apply_tg)+'">'+ICON_TG+'</a></div>'+
      '</article>';
  }).join(''):'<p class="empty">'+esc(T._empty)+'</p>';
  renderCities(); renderPins();
}
function renderFilters(){
  var box=$('filterList'); if(!box)return;
  var cats=[]; JOBS.forEach(function(j){if(cats.indexOf(j.cat)<0)cats.push(j.cat)});
  var opts=[['all',T._f_all]].concat(cats.map(function(c){return [c,(T._cat||{})[c]||c]}));
  if(JOBS.some(function(j){return j.house})&&!JOBS.every(function(j){return j.house}))opts.push(['house',T._f_house]);
  box.innerHTML=opts.map(function(o){return '<button type="button" data-f="'+esc(o[0])+'" aria-pressed="'+(o[0]===filter)+'">'+esc(o[1])+'</button>'}).join('');
}
var counts=function(){var c={};JOBS.filter(byCat).forEach(function(j){j.cities.forEach(function(k){c[k]=(c[k]||0)+1})});return c};
var usedCities=function(){var u=[];JOBS.forEach(function(j){j.cities.forEach(function(k){if(CITIES[k]&&u.indexOf(k)<0)u.push(k)})});return u};
function renderCities(){
  var box=$('cityList'); if(!box)return;
  var c=counts(), keys=usedCities().sort(function(a,b){return CITIES[b].ll[0]-CITIES[a].ll[0]});
  box.innerHTML='<button type="button" data-city="" aria-pressed="'+(!city)+'"><span>'+esc(T._allc)+'</span><b>'+JOBS.filter(byCat).length+'</b></button>'+
    keys.map(function(k){return '<button type="button" data-city="'+k+'" aria-pressed="'+(k===city)+'"'+(c[k]?'':' disabled')+'><span>'+esc(CITIES[k].name)+'</span><b>'+(c[k]||0)+'</b></button>'}).join('');
}
function selectCity(k){
  city=k||null;
  if(map){
    if(city)map.flyTo({center:lnglat(city),zoom:Math.max(map.getZoom(),11),duration:600});
    else map.fitBounds(allBounds(),{padding:pad(),duration:600});
  }
  renderJobs();
}

/* ---------- карта (MapLibre + OpenFreeMap, без подписей подложки; группы близких городов) ---------- */
var map=null, pins=[];
var lnglat=function(k){return [CITIES[k].ll[1],CITIES[k].ll[0]]};
var allBounds=function(){
  var u=usedCities(), b=new maplibregl.LngLatBounds(lnglat(u[0]),lnglat(u[0]));
  u.forEach(function(k){b.extend(lnglat(k))}); return b;
};
var pad=function(){var w=$('map').offsetWidth, x=Math.round(Math.min(100,w*.14));return {top:40,bottom:40,left:x,right:x}};
function initMap(){
  var el=$('map'); if(!el||!usedCities().length)return;
  var gl=false; try{var cv=document.createElement('canvas');gl=!!(cv.getContext('webgl2')||cv.getContext('webgl'))}catch(e){}
  if(!window.maplibregl||!gl){el.parentNode.classList.add('nomap');el.remove();return}
  try{
    map=new maplibregl.Map({container:el,style:'https://tiles.openfreemap.org/styles/positron',bounds:allBounds(),
      fitBoundsOptions:{padding:pad()},attributionControl:{compact:true},dragRotate:false,touchPitch:false,cooperativeGestures:true,minZoom:6,maxZoom:15});
  }catch(e){el.parentNode.classList.add('nomap');el.remove();map=null;return}
  map.addControl(new maplibregl.NavigationControl({showCompass:false}),rtl?'top-right':'top-left');
  map.touchZoomRotate.disableRotation();
  map.on('load',function(){
    map.getStyle().layers.forEach(function(l){if(l.type==='symbol')map.setLayoutProperty(l.id,'visibility','none')});
    renderPins();
  });
  map.on('zoomend',renderPins);
}
function renderPins(){
  if(!map)return;
  pins.forEach(function(p){p.remove()}); pins=[];
  var c=counts(), keys=usedCities(), used={}, R=52;
  var pt={}; keys.forEach(function(k){pt[k]=map.project(lnglat(k))});
  keys.sort(function(a,b){return (c[b]||0)-(c[a]||0)}).forEach(function(k){
    if(used[k])return;
    var g=[k]; used[k]=1;
    keys.forEach(function(o){if(!used[o]&&Math.hypot(pt[o].x-pt[k].x,pt[o].y-pt[k].y)<R){g.push(o);used[o]=1}});
    var n=JOBS.filter(function(j){return byCat(j)&&j.cities.some(function(x){return g.indexOf(x)>-1})}).length;
    var b=document.createElement('button'); b.type='button';
    var names=g.map(function(x){return CITIES[x].name}).join(', ');
    b.className='pinm'+(g.length>1?' group':'')+(g.indexOf(city)>-1&&g.length===1?' on':'')+(n?'':' zero');
    b.setAttribute('aria-label',names+': '+n);
    if(rtl)b.style.flexDirection='row-reverse';
    b.innerHTML='<b>'+n+'</b><span>'+esc(names)+'</span>';
    b.addEventListener('click',function(e){
      e.stopPropagation();
      if(g.length>1){var bb=new maplibregl.LngLatBounds(lnglat(g[0]),lnglat(g[0]));g.forEach(function(x){bb.extend(lnglat(x))});map.fitBounds(bb,{padding:pad(),maxZoom:13,duration:600})}
      else selectCity(city===k?null:k);
    });
    var single=g.length===1;
    var m=new maplibregl.Marker({element:b,anchor:single?(rtl?'right':'left'):'center',offset:single?[rtl?17:-17,0]:[0,0]})
      .setLngLat(lnglat(k)).addTo(map);
    pins.push(m);
  });
}

/* ---------- согласие на аналитику (Яндекс Метрика грузится только после «Разрешить») ---------- */
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
function loadMetrika(){
  if(!D.ym||window.ym)return;
  (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();
    k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
    (window,document,'script','https://mc.yandex.ru/metrika/tag.js?id='+D.ym,'ym');
  window.ym(D.ym,'init',{ssr:true,webvisor:true,clickmap:true,referrer:document.referrer,url:location.href,accurateTrackBounce:true,trackLinks:true});
}
function initConsent(){
  var box=$('consent'); if(!box)return;
  var v=store('dehr-consent');
  if(v==='yes'){loadMetrika();return}
  if(v==='no')return;
  box.hidden=false;
  box.addEventListener('click',function(e){
    var b=e.target.closest('[data-consent]'); if(!b)return;
    store('dehr-consent',b.dataset.consent); box.hidden=true;
    if(b.dataset.consent==='yes')loadMetrika();
  });
}

/* ---------- запуск ---------- */
var fl=$('filterList');
if(fl)fl.addEventListener('click',function(e){var b=e.target.closest('[data-f]');if(!b)return;filter=b.dataset.f;renderFilters();renderJobs()});
var cl=$('cityList');
if(cl)cl.addEventListener('click',function(e){var b=e.target.closest('[data-city]');if(b)selectCity(b.dataset.city)});
renderFilters(); initMap(); renderJobs(); initConsent();
if(location.hash.indexOf('#job-')===0){var t=document.querySelector(location.hash);if(t)t.scrollIntoView()}
})();
