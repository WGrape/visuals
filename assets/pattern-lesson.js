(function(){
  function init(root){
    const buttons=Array.from(root.querySelectorAll('[data-pattern-step]'));
    const roles=Array.from(root.querySelectorAll('[data-pattern-role]'));
    const title=root.querySelector('[data-scene-title]');
    const detail=root.querySelector('[data-scene-detail]');
    const progress=root.querySelector('[data-pattern-progress]');
    const play=root.querySelector('[data-pattern-play]');
    const roleDetail=root.querySelector('[data-role-detail]');
    if(!buttons.length||!title||!detail)return;
    let current=0,timer=null;
    function render(index){
      current=index;
      const chosen=buttons[index];
      buttons.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
      roles.forEach((role,i)=>role.classList.toggle('is-active',(chosen.dataset.active||'').split(',').includes(String(i))));
      title.textContent=chosen.dataset.title||chosen.textContent;
      detail.textContent=chosen.dataset.detail||'';
      if(progress)progress.style.width=((index+1)/buttons.length*100)+'%';
    }
    function stop(){if(timer){clearInterval(timer);timer=null;}if(play){play.textContent='▶ 自动播放';play.setAttribute('aria-pressed','false');}}
    buttons.forEach((button,i)=>button.addEventListener('click',()=>{stop();render(i);}));
    if(roleDetail&&roles.length){
      function showRole(index){
        roles.forEach((role,i)=>role.classList.toggle('is-focused',i===index));
        roleDetail.textContent=roles[index].dataset.roleNote||'';
      }
      roles.forEach((role,i)=>role.addEventListener('click',()=>showRole(i)));
      showRole(0);
    }
    if(play)play.addEventListener('click',()=>{
      if(timer){stop();return;}
      play.textContent='Ⅱ 暂停';play.setAttribute('aria-pressed','true');
      render(0);
      timer=setInterval(()=>{if(current===buttons.length-1){stop();return;}render(current+1);},1700);
    });
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    render(0);
  }
  document.querySelectorAll('[data-pattern-lesson]').forEach(init);
  document.querySelectorAll('[data-pattern-lab]').forEach(root=>{
    const options=Array.from(root.querySelectorAll('[data-lab-option]'));
    const route=root.querySelector('[data-lab-route]');
    const result=root.querySelector('[data-lab-result]');
    const why=root.querySelector('[data-lab-why]');
    if(!options.length||!route||!result||!why)return;
    function show(index){
      const option=options[index];
      options.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
      route.replaceChildren();
      (option.dataset.route||'').split('>').filter(Boolean).forEach((name,i)=>{
        if(i){const arrow=document.createElement('span');arrow.className='pattern-lab-arrow';arrow.setAttribute('aria-hidden','true');arrow.textContent='→';route.append(arrow);}
        const node=document.createElement('span');node.className='pattern-lab-node';node.style.animationDelay=(i*110)+'ms';node.textContent=name;route.append(node);
      });
      result.textContent=option.dataset.result||'';
      why.textContent=option.dataset.why||'';
    }
    options.forEach((option,i)=>option.addEventListener('click',()=>show(i)));
    show(0);
  });
})();
