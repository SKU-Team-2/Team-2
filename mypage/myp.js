document.addEventListener('DOMContentLoaded', function () {
  var sliderIndex = 0;
  var sliderItems = document.querySelectorAll('.slider-item');
  var sliderWrapper = document.querySelector('.slider-wrapper');
  var prevBtn = document.querySelector('.carousel-control-prev');
  var nextBtn = document.querySelector('.carousel-control-next');
  var slideAutoInterval;

  function changeSlider(index) {
      sliderWrapper.style.transform = 'translateX(' + (-index * 100) + '%)';
  }

  function prevSlider() {
      sliderIndex--;

      if (sliderIndex < 0) {
          sliderIndex = sliderItems.length - 1;
      }

      changeSlider(sliderIndex);
  }

  function nextSlider() {
      sliderIndex++;

      if (sliderIndex >= sliderItems.length) {
          sliderIndex = 0;
      }

      changeSlider(sliderIndex);
  }

  prevBtn.addEventListener('click', prevSlider);
  nextBtn.addEventListener('click', nextSlider);

  function startAutoSlide() {
      slideAutoInterval = setInterval(nextSlider, 2000);
  }

  startAutoSlide();
});