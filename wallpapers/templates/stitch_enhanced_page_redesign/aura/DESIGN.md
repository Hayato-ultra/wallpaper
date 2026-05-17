---
name: Aura
colors:
  surface: '#151317'
  surface-dim: '#151317'
  surface-bright: '#3b383d'
  surface-container-lowest: '#0f0d11'
  surface-container-low: '#1d1b1f'
  surface-container: '#211f23'
  surface-container-high: '#2c292d'
  surface-container-highest: '#373438'
  on-surface: '#e7e1e6'
  on-surface-variant: '#cbc4ce'
  inverse-surface: '#e7e1e6'
  inverse-on-surface: '#322f34'
  outline: '#948f98'
  outline-variant: '#49454d'
  surface-tint: '#d0bfec'
  primary: '#d0bfec'
  on-primary: '#362a4d'
  primary-container: '#7e7098'
  on-primary-container: '#ffffff'
  inverse-primary: '#65587e'
  secondary: '#cbc4ce'
  on-secondary: '#322f36'
  secondary-container: '#49454d'
  on-secondary-container: '#b9b3bc'
  tertiary: '#c7c5cc'
  on-tertiary: '#303035'
  tertiary-container: '#76767c'
  on-tertiary-container: '#ffffff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ebddff'
  primary-fixed-dim: '#d0bfec'
  on-primary-fixed: '#211537'
  on-primary-fixed-variant: '#4d4065'
  secondary-fixed: '#e7e0ea'
  secondary-fixed-dim: '#cbc4ce'
  on-secondary-fixed: '#1d1a21'
  on-secondary-fixed-variant: '#49454d'
  tertiary-fixed: '#e3e1e8'
  tertiary-fixed-dim: '#c7c5cc'
  on-tertiary-fixed: '#1b1b20'
  on-tertiary-fixed-variant: '#46464c'
  background: '#151317'
  on-background: '#e7e1e6'
  surface-variant: '#373438'
typography:
  display-lg:
    fontFamily: Manrope
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Manrope
    fontSize: 36px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.4'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 48px
  xl: 80px
  gutter: 24px
  margin-mobile: 20px
  margin-desktop: 64px
---

## Brand & Style

The design system is centered on a philosophy of "Atmospheric Minimalism." It is designed to recede into the background, allowing high-fidelity visual content—specifically wallpapers and digital art—to command the user's attention. The aesthetic is sophisticated, moody, and premium, targeting an audience that appreciates editorial-grade digital experiences.

The style leans heavily into **Glassmorphism** and **Modern Minimalism**. Rather than using traditional shadows to define depth, it utilizes semi-transparent layers, high-density backdrop blurs, and ultra-fine "inner-glow" borders to create a sense of physical stacks. The emotional response is intended to be one of calm, focus, and quiet luxury.

## Colors

The palette is anchored by a deep, monochromatic foundation to maximize contrast with featured imagery. 

- **Primary:** A muted, desaturated purple (#7e7098) used sparingly for interactive highlights and active states. It is intended to feel like a soft glow rather than a piercing neon.
- **Surface:** The core background is a deep charcoal-black (#0f0d11). 
- **Accents:** Secondary surfaces utilize a slightly lifted charcoal (#2a272e) for container nesting. 
- **Typography:** The primary text color is a soft off-white (#e2e0e7) to reduce eye strain in dark environments while maintaining high legibility.

## Typography

This design system utilizes **Manrope** across all roles to maintain a cohesive, modern, and highly legible interface. The type scale is built on a modular rhythm, prioritizing generous line heights for body text to enhance the "airy" feel of the interface.

Headlines use tighter tracking and heavier weights to provide a strong structural anchor against the soft-edged glass UI elements. Labels and metadata should be treated with increased letter spacing and semi-bold weights to ensure they remain distinct even at small sizes.

## Layout & Spacing

The layout philosophy follows a **fixed-center grid** for desktop and a **fluid grid** for mobile. The system emphasizes "Purposeful Whitespace"—using larger-than-standard gaps (48px+) between major sections to prevent the dark UI from feeling cramped or heavy.

- **Desktop:** 12-column grid with a 1200px max-width container, 24px gutters, and 64px side margins.
- **Mobile:** 4-column fluid grid with 20px side margins.
- **Rhythm:** All vertical spacing must be a multiple of the 8px base unit. Component-internal spacing (padding) should be generous to reinforce the premium feel.

## Elevation & Depth

Depth is established through **Refined Glassmorphism** rather than traditional drop shadows. This simulates a series of translucent panels floating over the background content.

1.  **Backdrop Blur:** All elevated panels must apply a `backdrop-filter: blur(24px)`.
2.  **Surface Opacity:** Floating containers use a background color of `rgba(42, 39, 46, 0.6)`.
3.  **Subtle Borders:** Panels are defined by a 1px solid border. The border color should be a light-tinted white with very low opacity (`rgba(255, 255, 255, 0.1)`).
4.  **Tonal Stacking:** For nested elements, increase the background opacity by 10% for each subsequent layer rather than adding shadows.

## Shapes

The shape language is consistently **Rounded**, avoiding both the clinical feel of sharp corners and the playfulness of pill shapes. 

- **Components:** Standard buttons, input fields, and small cards use a 0.5rem (8px) radius.
- **Containers:** Large content cards and modal windows use the `rounded-lg` (16px) or `rounded-xl` (24px) tokens to create a softer, frame-like appearance for the featured visuals.
- **Consistency:** Interaction states (hovers, focus) should maintain the same corner radius as the base element to avoid visual jarring.

## Components

### Buttons
Primary buttons use the muted purple accent (#7e7098) with white text. Secondary buttons should be "Glass Buttons"—fully transparent with the standard 1px subtle border and backdrop blur.

### Cards
Cards are the primary vehicle for content. They should have no visible background when empty, taking on the glass properties only when containing content. The 1px border is mandatory to separate imagery from the charcoal background.

### Input Fields
Inputs are minimalist: a subtle dark background (`#1a181d`) with a 1px bottom border that transitions to the primary purple on focus. Avoid full-box outlines unless the input is placed directly over a complex image.

### Chips & Tags
Chips are small, fully rounded (pill-style) elements with a `20%` opacity primary purple fill and `100%` opacity text. They should feel like soft highlights.

### Lists
List items are separated by thin, low-contrast lines (`rgba(255, 255, 255, 0.05)`). Hover states should trigger a subtle lift in background brightness rather than a color change.