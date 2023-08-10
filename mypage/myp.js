const sliderWrapper = document.querySelector('.slider-wrapper');
const sliderItems = document.querySelector('.slider-items');
const sliderItem = document.querySelectorAll('.slider-item');
const sliderItemWidth = sliderItem[0].offsetWidth;
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');

let currentSlide = 0; // 현재 슬라이드 인덱스
const slideInterval = 3000; // 슬라이드 간격 (ms)

// 슬라이드 이동 함수
function moveSlides() {
  // 현재 슬라이드 인덱스를 증가
  currentSlide++;
  
  // sliderItems를 이동시키는 transform 속성 값을 조정하여 슬라이드 이동
  sliderItems.style.transform = `translateX(-${currentSlide * sliderItemWidth}px)`;
  
  // 마지막 슬라이드에서 처음 슬라이드로 돌아가도록 설정
  if (currentSlide >= sliderItem.length - 0.001) {
    // 0.01초 후에 첫 슬라이드로 이동
    setTimeout(() => {
      sliderItems.style.transition = 'transform 0ms ease-in-out';
      sliderItems.style.transform = 'translateX(0)';
      currentSlide = 0;
      // 슬라이드 이동 애니메이션을 다시 적용
      setTimeout(() => {
        sliderItems.style.transition = '';
      }, 100);
    }, 1000);
  }
}

// slideInterval 간격으로 moveSlides 함수 호출
setInterval(moveSlides, slideInterval);

prevBtn.addEventListener('click', () => {
  if (currentSlide === 0) {
    currentSlide = sliderItem.length - 1;
  } else {
    currentSlide--;
  }
  sliderItems.style.transform = `translateX(-${currentSlide * sliderItemWidth}px)`;
});

nextBtn.addEventListener('click', () => {
  if (currentSlide === sliderItem.length - 1) {
    currentSlide = 0;
  } else {
    currentSlide++;
  }
  sliderItems.style.transform = `translateX(-${currentSlide * sliderItemWidth}px)`;
});
