document.querySelectorAll('[data-stepper]').forEach(stepper => {
  const buttons = [...stepper.querySelectorAll('[data-step-button]')];
  const panels = [...stepper.querySelectorAll('[data-step-panel]')];
  function show(index) {
    buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
    panels.forEach((panel, i) => { panel.hidden = i !== index; });
  }
  buttons.forEach((button, index) => button.addEventListener('click', () => show(index)));
  show(0);
});
