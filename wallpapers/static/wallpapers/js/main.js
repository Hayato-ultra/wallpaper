// Wallpaper Haven - Aura Design System

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
  initSkeletonLoader()
  initPageTransition()
  initCountUp()
  initImageZoom()
  initProgressiveImage()
  initCategoryDropdown()
  initMobileFilters()
  initSearchBar()
  initInfiniteScroll()
})

/* ── Mobile Menu ── */
function initMobileMenu() {
  const toggle = document.getElementById('mobile-menu-toggle')
  const menu = document.getElementById('mobile-menu')
  if (!toggle || !menu) return

  toggle.addEventListener('click', function () {
    const isHidden = menu.classList.toggle('hidden')
    const icon = toggle.querySelector('.material-symbols-outlined')
    if (icon) icon.textContent = isHidden ? 'menu' : 'close'
  })
}

/* ── Image Preview on Upload ── */
function initImagePreview() {
  const fileInput = document.getElementById('id_file')
  const preview = document.getElementById('preview')
  const dropZone = document.getElementById('drop-zone')
  const fileName = document.getElementById('file-name')
  if (!fileInput || !preview || !dropZone) return

  fileInput.addEventListener('change', function (e) {
    const file = e.target.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = function (ev) {
      preview.src = ev.target.result
      const placeholder = dropZone.querySelector('.upload-placeholder')
      if (placeholder) placeholder.style.display = 'none'
      const info = dropZone.querySelector('.upload-info')
      if (info) info.classList.remove('hidden')
      if (fileName) fileName.textContent = file.name
    }
    reader.readAsDataURL(file)
  })

  dropZone.addEventListener('dragover', function (e) {
    e.preventDefault()
    dropZone.classList.add('border-primary', 'bg-primary/10', 'scale-[1.02]')
  })
  dropZone.addEventListener('dragleave', function () {
    dropZone.classList.remove('border-primary', 'bg-primary/10', 'scale-[1.02]')
  })
  dropZone.addEventListener('drop', function (e) {
    e.preventDefault()
    dropZone.classList.remove('border-primary', 'bg-primary/10', 'scale-[1.02]')
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files
      fileInput.dispatchEvent(new Event('change'))
    }
  })
}

/* ── Lazy Loading ── */
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
        el.classList.add('text-primary')
        setTimeout(function () {
          el.textContent = orig
          el.classList.remove('text-primary')
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

/* ── Progressive Image ── */
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

/* ── Searchable Category Dropdown ── */
function initCategoryDropdown() {
  var container = document.getElementById('category-dropdown')
  var searchInput = document.getElementById('category-search')
  var hiddenInput = document.getElementById('category-value')
  var optionsContainer = document.getElementById('category-options')
  if (!container || !searchInput || !hiddenInput || !optionsContainer) return

  var categories = (typeof CATEGORIES !== 'undefined') ? CATEGORIES : []

  function renderOptions(filter) {
    var q = (filter || '').toLowerCase()
    var matches = categories.filter(function (c) { return c.toLowerCase().includes(q) })
    if (matches.length === 0) {
      optionsContainer.innerHTML = '<div class="px-4 py-3 text-sm text-on-surface-variant">No matching categories</div>'
      return
    }
    var html = ''
    for (var i = 0; i < matches.length; i++) {
      html += '<div class="category-option px-4 py-2.5 text-sm text-on-surface-variant hover:bg-white/5 hover:text-on-surface cursor-pointer transition-colors" data-value="' + matches[i] + '">' + matches[i] + '</div>'
    }
    optionsContainer.innerHTML = html
    optionsContainer.querySelectorAll('.category-option').forEach(function (opt) {
      opt.addEventListener('click', function () {
        selectCategory(opt.dataset.value)
      })
    })
  }

  function selectCategory(value) {
    searchInput.value = value
    hiddenInput.value = value
    optionsContainer.classList.add('hidden')
    optionsContainer.innerHTML = ''
  }

  searchInput.addEventListener('focus', function () {
    renderOptions(searchInput.value)
    optionsContainer.classList.remove('hidden')
  })

  searchInput.addEventListener('input', function () {
    hiddenInput.value = ''
    renderOptions(searchInput.value)
    optionsContainer.classList.remove('hidden')
  })

  document.addEventListener('click', function (e) {
    if (!container.contains(e.target)) {
      optionsContainer.classList.add('hidden')
    }
  })

  searchInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault()
      hiddenInput.value = searchInput.value
      optionsContainer.classList.add('hidden')
    }
    if (e.key === 'Escape') {
      optionsContainer.classList.add('hidden')
    }
  })
}

/* ── Mobile Filters Toggle ── */
function initMobileFilters() {
  var container = document.getElementById('mobile-filters')
  if (!container) return

  document.addEventListener('click', function (e) {
    if (!container.open) return
    if (!container.contains(e.target)) {
      container.removeAttribute('open')
    }
  })
}

/* ── Inline Search Bar ── */
function initSearchBar() {
  var btn = document.getElementById('search-btn')
  var bar = document.getElementById('search-bar')
  var input = document.getElementById('search-input')
  var suggestions = document.getElementById('search-suggestions')
  var iconOpen = document.getElementById('search-icon-open')
  var iconClose = document.getElementById('search-icon-close')
  if (!btn || !bar || !input || !suggestions || !iconOpen || !iconClose) return

  var isOpen = false
  var categories = (typeof SEARCH_CATEGORIES !== 'undefined' && SEARCH_CATEGORIES.length) ? SEARCH_CATEGORIES : ['cars', 'anime', 'nature', 'dark']
  var catIndex = 0
  var catTimer = null

  function cyclePlaceholder() {
    if (!isOpen) return
    var cat = categories[catIndex]
    input.placeholder = 'Search ' + cat + '...'
    catIndex = (catIndex + 1) % categories.length
    catTimer = setTimeout(cyclePlaceholder, 2500)
  }

  function openSearch() {
    isOpen = true
    bar.style.maxWidth = '280px'
    bar.style.opacity = '1'
    bar.style.visibility = 'visible'
    iconOpen.classList.add('hidden')
    iconClose.classList.remove('hidden')
    suggestions.classList.remove('hidden')
    setTimeout(function () { input.focus(); cyclePlaceholder() }, 300)
  }

  function closeSearch() {
    isOpen = false
    clearTimeout(catTimer)
    bar.style.maxWidth = '0'
    bar.style.opacity = '0'
    bar.style.visibility = 'hidden'
    iconOpen.classList.remove('hidden')
    iconClose.classList.add('hidden')
    suggestions.classList.add('hidden')
    input.value = ''
    input.placeholder = 'Search wallpapers...'
  }

  function submitSearch(q) {
    if (q && q.trim()) {
      window.location.href = '/search/?q=' + encodeURIComponent(q.trim())
    }
  }

  btn.addEventListener('click', function (e) {
    e.stopPropagation()
    if (isOpen) {
      closeSearch()
    } else {
      openSearch()
    }
  })

  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault()
      submitSearch(input.value)
    }
    if (e.key === 'Escape') {
      closeSearch()
    }
  })

  document.querySelectorAll('.suggestion-chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
      submitSearch(chip.dataset.q)
    })
  })

  document.addEventListener('click', function (e) {
    if (!isOpen) return
    var root = document.getElementById('search-root')
    if (root && !root.contains(e.target)) {
      closeSearch()
    }
  })
}

/* ── Infinite Scroll ── */
function initInfiniteScroll() {
  var sentinel = document.getElementById('scroll-sentinel')
  var grid = document.getElementById('wallpaper-grid')
  if (!sentinel || !grid) return
  if (!sentinel.dataset.next) return

  var loading = false

  function buildUrl(page) {
    var url = new URL(window.location.href)
    url.searchParams.set('page', page)
    url.searchParams.set('ajax', '1')
    return url.pathname + '?' + url.searchParams.toString()
  }

  var observer = new IntersectionObserver(function (entries) {
    if (!entries[0].isIntersecting) return
    if (loading) return
    var next = sentinel.dataset.next
    if (!next) return

    loading = true

    var xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
      if (xhr.readyState !== 4) return
      loading = false
      if (xhr.status !== 200) return

      var temp = document.createElement('div')
      temp.innerHTML = xhr.responseText

      var newItems = temp.querySelectorAll('#wallpaper-grid > *')
      newItems.forEach(function (el) { grid.appendChild(el) })

      var newSentinel = temp.getElementById('scroll-sentinel')
      if (newSentinel) {
        sentinel.dataset.next = newSentinel.dataset.next || ''
        sentinel.dataset.page = newSentinel.dataset.page
        if (!newSentinel.dataset.next) {
          sentinel.dataset.next = ''
          observer.unobserve(sentinel)
        }
      }
    }
    xhr.open('GET', buildUrl(next), true)
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
    xhr.send()
  }, { rootMargin: '400px' })

  observer.observe(sentinel)
}
