// Wallpaper Haven - Main JavaScript

document.addEventListener('DOMContentLoaded', function () {
  initMobileMenu()
  initImagePreview()
  initLazyLoading()
  initFilterChips()
  initSearchDebounce()
  initCopyColor()
  initSmoothScroll()
  initToastDismiss()
  initScrollReveal()
  initParallaxHero()
  initSkeletonLoader()
  initPageTransition()
  initCountUp()
  initImageZoom()
  initProgressiveImage()
})

/* ── Mobile Menu ── */
function initMobileMenu() {
  const toggle = document.getElementById('mobile-menu-toggle')
  const menu = document.getElementById('mobile-menu')
  if (!toggle || !menu) return

  toggle.addEventListener('click', function () {
    const isHidden = menu.classList.toggle('hidden')
    toggle.innerHTML = isHidden
      ? '<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>'
      : '<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>'
  })
}

/* ── Image Preview on Upload ── */
function initImagePreview() {
  const fileInput = document.getElementById('id_file')
  const preview = document.getElementById('preview')
  const dropZone = document.getElementById('drop-zone')
  if (!fileInput || !preview || !dropZone) return

  fileInput.addEventListener('change', function (e) {
    const file = e.target.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = function (ev) {
      preview.src = ev.target.result
      preview.classList.remove('hidden')
      const placeholder = dropZone.querySelector('.upload-placeholder')
      if (placeholder) placeholder.style.display = 'none'
    }
    reader.readAsDataURL(file)
  })

  dropZone.addEventListener('click', function () {
    fileInput.click()
  })

  dropZone.addEventListener('dragover', function (e) {
    e.preventDefault()
    dropZone.classList.add('border-blue-500', 'bg-blue-500/10', 'scale-[1.02]')
  })
  dropZone.addEventListener('dragleave', function () {
    dropZone.classList.remove('border-blue-500', 'bg-blue-500/10', 'scale-[1.02]')
  })
  dropZone.addEventListener('drop', function (e) {
    e.preventDefault()
    dropZone.classList.remove('border-blue-500', 'bg-blue-500/10', 'scale-[1.02]')
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files
      fileInput.dispatchEvent(new Event('change'))
    }
  })
}

/* ── Lazy Loading with Intersection Observer ── */
function initLazyLoading() {
  if (!('IntersectionObserver' in window)) return

  const lazyImages = document.querySelectorAll('img[data-src]')
  lazyImages.forEach(function (img) { observeImage(img) })

  const lazyCards = document.querySelectorAll('.lazy-card')
  if (lazyCards.length) {
    const cardObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in')
          cardObserver.unobserve(entry.target)
        }
      })
    }, { rootMargin: '100px' })
    lazyCards.forEach(function (card) { cardObserver.observe(card) })
  }
}

function observeImage(img) {
  if (!('IntersectionObserver' in window)) { img.src = img.dataset.src; return }
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        img.src = img.dataset.src
        img.removeAttribute('data-src')
        observer.unobserve(img)
        img.classList.add('loaded')
      }
    })
  }, { rootMargin: '300px', threshold: 0.01 })
  observer.observe(img)
}

/* ── Filter Chips ── */
function initFilterChips() {
  document.querySelectorAll('.filter-chip').forEach(function (chip) {
    chip.addEventListener('click', function (e) {
      if (chip.tagName === 'A') return
      e.preventDefault()
      window.location.href = chip.dataset.href || chip.getAttribute('href')
    })
  })
}

/* ── Search Debounce ── */
function initSearchDebounce() {
  const searchInput = document.querySelector('input[name="q"]')
  const searchForm = searchInput?.closest('form')
  if (!searchInput || !searchForm) return

  let timeout
  searchInput.addEventListener('input', function () {
    clearTimeout(timeout)
    timeout = setTimeout(function () {
      if (searchInput.value.trim().length >= 2) {
        searchForm.submit()
      }
    }, 600)
  })
}

/* ── Copy Color ── */
function initCopyColor() {
  document.querySelectorAll('[data-copy]').forEach(function (el) {
    el.addEventListener('click', function () {
      const text = el.dataset.copy
      if (!navigator.clipboard) return
      navigator.clipboard.writeText(text).then(function () {
        const orig = el.textContent
        el.textContent = 'Copied!'
        el.classList.add('text-green-400')
        setTimeout(function () {
          el.textContent = orig
          el.classList.remove('text-green-400')
        }, 1500)
      })
    })
  })
}

/* ── Smooth Scroll ── */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      const href = a.getAttribute('href')
      if (href === '#') return
      const target = document.querySelector(href)
      if (target) {
        e.preventDefault()
        target.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    })
  })
}

/* ── Toast Dismiss ── */
function initToastDismiss() {
  document.querySelectorAll('.toast-dismiss').forEach(function (btn) {
    btn.addEventListener('click', function () {
      btn.closest('.toast')?.remove()
    })
  })
  document.querySelectorAll('.toast').forEach(function (toast) {
    setTimeout(function () { toast?.remove() }, 5000)
  })
}

/* ── Scroll Reveal Animations ── */
function initScrollReveal() {
  if (!('IntersectionObserver' in window)) return
  const els = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-up')
  if (!els.length) return

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed')
        observer.unobserve(entry.target)
      }
    })
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' })

  els.forEach(function (el) { observer.observe(el) })
}

/* ── Parallax Hero ── */
function initParallaxHero() {
  const hero = document.querySelector('.parallax-hero')
  if (!hero) return
  window.addEventListener('scroll', function () {
    const scrollY = window.scrollY
    if (scrollY < window.innerHeight) {
      hero.style.transform = 'translateY(' + (scrollY * 0.3) + 'px)'
      hero.style.opacity = 1 - (scrollY / window.innerHeight) * 0.5
    }
  }, { passive: true })
}

/* ── Skeleton Loader ── */
function initSkeletonLoader() {
  document.querySelectorAll('.skeleton-loader').forEach(function (el) {
    const img = el.querySelector('img')
    if (img) {
      img.classList.add('opacity-0')
      img.addEventListener('load', function () {
        img.classList.remove('opacity-0')
        img.classList.add('opacity-100', 'transition-opacity', 'duration-500')
        el.classList.remove('skeleton-loader')
        el.classList.add('skeleton-loaded')
      })
      if (img.complete) {
        img.classList.remove('opacity-0')
        img.classList.add('opacity-100')
        el.classList.remove('skeleton-loader')
        el.classList.add('skeleton-loaded')
      }
    }
  })
}

/* ── Page Transition ── */
function initPageTransition() {
  document.querySelectorAll('a.animate-transition').forEach(function (link) {
    link.addEventListener('click', function (e) {
      const href = link.getAttribute('href')
      if (!href || href.startsWith('#') || href.startsWith('http')) return
      e.preventDefault()
      document.body.classList.add('page-exit')
      setTimeout(function () { window.location.href = href }, 300)
    })
  })
}

/* ── Count Up Animation ── */
function initCountUp() {
  document.querySelectorAll('.count-up').forEach(function (el) {
    const target = parseInt(el.dataset.target) || 0
    const duration = parseInt(el.dataset.duration) || 1500
    if (target === 0) { el.textContent = '0'; return }
    if (!('IntersectionObserver' in window)) { el.textContent = target; return }

    const observer = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) {
        observer.unobserve(el)
        const start = performance.now()
        function update(now) {
          const progress = Math.min((now - start) / duration, 1)
          const eased = 1 - Math.pow(1 - progress, 3)
          el.textContent = Math.floor(eased * target).toLocaleString()
          if (progress < 1) requestAnimationFrame(update)
        }
        requestAnimationFrame(update)
      }
    }, { threshold: 0.5 })
    observer.observe(el)
  })
}

/* ── Image Zoom on Detail Page ── */
function initImageZoom() {
  const viewer = document.querySelector('.image-zoom-container')
  if (!viewer) return
  const img = viewer.querySelector('img')
  if (!img) return

  let zoomed = false
  viewer.addEventListener('click', function () {
    zoomed = !zoomed
    viewer.classList.toggle('zoomed', zoomed)
    img.style.cursor = zoomed ? 'zoom-out' : 'zoom-in'
  })

  viewer.addEventListener('mousemove', function (e) {
    if (!zoomed) return
    const rect = viewer.getBoundingClientRect()
    const x = ((e.clientX - rect.left) / rect.width) * 100
    const y = ((e.clientY - rect.top) / rect.height) * 100
    img.style.transformOrigin = x + '% ' + y + '%'
  })
}

/* ── Progressive Image: blur placeholder -> full image ── */
function initProgressiveImage() {
  var img = document.querySelector('.progressive-img img.full[data-progressive]')
  if (!img) return

  var placeholder = img.parentElement.querySelector('.placeholder')
  var fullSrc = img.getAttribute('data-src')

  var loader = new Image()
  loader.onload = function () {
    img.src = fullSrc
    img.classList.add('loaded')
    if (placeholder) placeholder.classList.add('hidden')
  }
  loader.onerror = function () {
    img.src = fullSrc
    img.classList.add('loaded')
    if (placeholder) placeholder.classList.add('hidden')
  }
  if (loader.complete) {
    img.src = fullSrc
    img.classList.add('loaded')
    if (placeholder) placeholder.classList.add('hidden')
  } else {
    loader.src = fullSrc
  }
}
