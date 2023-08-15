document.querySelectorAll('input').forEach((input) => {
  input.addEventListener('invalid', (e) => {
    e.target.classList.add('is--invalid');
  });
  input.addEventListener('valid', (e) => {
    e.target.classList.remove('is--invalid');
  });
});
