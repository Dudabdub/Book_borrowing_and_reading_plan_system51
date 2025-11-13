document.addEventListener('DOMContentLoaded', function(){
  // fetch stats for dashboard (if present)
  if (location.pathname === '/') {
    fetch('/api/stats').then(r=>r.json()).then(data=>{
      console.log('stats', data);
      // could render charts
    }).catch(()=>{});
  }
});
