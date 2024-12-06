document.addEventListener("DOMContentLoaded", function() {
      var mySwiper = new Swiper('.swiper', {
        loop: true,
        autoplay: {
          delay: 2500,
          disableOnInteraction: false,
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        },
      });
    });