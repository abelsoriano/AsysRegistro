(function() {
  "use strict";

  // Mantener las funciones auxiliares
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  // Envolver todas las inicializaciones en verificaciones de existencia
  window.addEventListener('load', () => {
    // Navbar links
    let navbarlinks = select('#navbar .scrollto', true)
    if (navbarlinks.length > 0) {
      const navbarlinksActive = () => {
        let position = window.scrollY + 200
        navbarlinks.forEach(navbarlink => {
          if (!navbarlink.hash) return
          let section = select(navbarlink.hash)
          if (!section) return
          if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
            navbarlink.classList.add('active')
          } else {
            navbarlink.classList.remove('active')
          }
        })
      }
      window.addEventListener('load', navbarlinksActive)
      onscroll(document, navbarlinksActive)
    }

    // Header scroll
    let selectHeader = select('#header')
    let selectTopbar = select('#topbar')
    if (selectHeader) {
      const headerScrolled = () => {
        if (window.scrollY > 100) {
          selectHeader.classList.add('header-scrolled')
          if (selectTopbar) {
            selectTopbar.classList.add('topbar-scrolled')
          }
        } else {
          selectHeader.classList.remove('header-scrolled')
          if (selectTopbar) {
            selectTopbar.classList.remove('topbar-scrolled')
          }
        }
      }
      window.addEventListener('load', headerScrolled)
      onscroll(document, headerScrolled)
    }

    // Back to top button
    let backtotop = select('.back-to-top')
    if (backtotop) {
      const toggleBacktotop = () => {
        if (window.scrollY > 100) {
          backtotop.classList.add('active')
        } else {
          backtotop.classList.remove('active')
        }
      }
      window.addEventListener('load', toggleBacktotop)
      onscroll(document, toggleBacktotop)
    }

    // Preloader
    let preloader = select('#preloader');
    if (preloader) {
      preloader.remove()
    }

    // Carousel indicators
    let heroCarouselIndicators = select("#hero-carousel-indicators")
    let heroCarouselItems = select('#heroCarousel .carousel-item', true)
    if (heroCarouselIndicators && heroCarouselItems.length > 0) {
      heroCarouselItems.forEach((item, index) => {
        (index === 0) ?
        heroCarouselIndicators.innerHTML += "<li data-bs-target='#heroCarousel' data-bs-slide-to='" + index + "' class='active'></li>":
          heroCarouselIndicators.innerHTML += "<li data-bs-target='#heroCarousel' data-bs-slide-to='" + index + "'></li>"
      });
    }

    // Inicializar Swiper solo si existe
    if (typeof Swiper !== 'undefined') {
      // Testimonials slider
      const testimonialSlider = select('.testimonials-slider');
      if (testimonialSlider) {
        new Swiper('.testimonials-slider', {
          speed: 600,
          loop: true,
          autoplay: {
            delay: 5000,
            disableOnInteraction: false
          },
          slidesPerView: 'auto',
          pagination: {
            el: '.swiper-pagination',
            type: 'bullets',
            clickable: true
          },
          breakpoints: {
            320: {
              slidesPerView: 1,
              spaceBetween: 20
            },
            1200: {
              slidesPerView: 3,
              spaceBetween: 20
            }
          }
        });
      }

      // Gallery slider
      const gallerySlider = select('.gallery-slider');
      if (gallerySlider) {
        new Swiper('.gallery-slider', {
          speed: 400,
          loop: true,
          centeredSlides: true,
          autoplay: {
            delay: 5000,
            disableOnInteraction: false
          },
          slidesPerView: 'auto',
          pagination: {
            el: '.swiper-pagination',
            type: 'bullets',
            clickable: true
          },
          breakpoints: {
            320: {
              slidesPerView: 1,
              spaceBetween: 20
            },
            640: {
              slidesPerView: 3,
              spaceBetween: 20
            },
            992: {
              slidesPerView: 5,
              spaceBetween: 20
            }
          }
        });
      }
    }

    // Inicializar GLightbox solo si existe
    if (typeof GLightbox !== 'undefined') {
      const galleryLightbox = GLightbox({
        selector: '.gallery-lightbox'
      });
    }

    // Inicializar AOS solo si existe
    if (typeof AOS !== 'undefined') {
      AOS.init({
        duration: 1000,
        easing: 'ease-in-out',
        once: true,
        mirror: false
      });
    }

    // Inicializar PureCounter solo si existe
    if (typeof PureCounter !== 'undefined') {
      new PureCounter();
    }
  });

  // Mobile nav toggle
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  // Mobile nav dropdowns
  on('click', '.navbar .dropdown > a', function(e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  // Scroll handling
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      e.preventDefault()
      let navbar = select('#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

})();