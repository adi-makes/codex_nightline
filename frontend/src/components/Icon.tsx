export type IconName = 'home' | 'search' | 'sparkles' | 'bag' | 'user' | 'pin' | 'food' | 'train' | 'calendar' | 'beach' | 'shop' | 'hotel' | 'mic' | 'send' | 'camera' | 'location' | 'plus' | 'heart' | 'directions' | 'chevron' | 'back' | 'clock' | 'map' | 'settings' | 'bookmark' | 'more' | 'star' | 'sliders' | 'zoomIn' | 'zoomOut' | 'share' | 'phone' | 'arrow'

export function Icon({ name, size = 21 }: { name: IconName; size?: number }) {
  const props = { width: size, height: size, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 1.9, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const }
  const paths: Record<IconName, React.ReactNode> = {
    home: <path d="m3.5 10 8.5-7 8.5 7v10.5H14v-6H10v6H3.5Z" />,
    search: <><circle cx="10.8" cy="10.8" r="5.8" /><path d="m16 16 4.2 4.2" /></>,
    sparkles: <><path d="m12 2 1.4 5.1L18.5 8.5l-5.1 1.4L12 15l-1.4-5.1-5.1-1.4 5.1-1.4Z" /><path d="m19 14 .7 2.3L22 17l-2.3.7L19 20l-.7-2.3L16 17l2.3-.7Z" /></>,
    bag: <><path d="M5 8h14l-1 13H6Z" /><path d="M9 9V6a3 3 0 0 1 6 0v3" /></>,
    user: <><circle cx="12" cy="7.7" r="3.3" /><path d="M5 21c.7-4 3.1-6 7-6s6.3 2 7 6" /></>,
    pin: <><path d="M20 10c0 5-8 11-8 11s-8-6-8-11a8 8 0 1 1 16 0Z" /><circle cx="12" cy="10" r="2.5" /></>,
    food: <><path d="M4 3v8a3 3 0 0 0 6 0V3M7 3v18M14 3v7a3 3 0 0 0 6 0V3M17 10v11" /></>,
    train: <><rect x="5" y="3" width="14" height="15" rx="4" /><path d="M8 21h8M9 18l-2 3M15 18l2 3M8.5 8h.01M15.5 8h.01M5 13h14" /></>,
    calendar: <><rect x="4" y="5" width="16" height="15" rx="2" /><path d="M8 3v4M16 3v4M4 10h16" /></>,
    beach: <><path d="M3 20h18M7 17a5 5 0 0 1 10 0M12 4v13M12 4c-3 0-5 2-5 4 3 0 5-2 5-7ZM12 4c3 0 5 2 5 4-3 0-5-2-5-4Z" /></>,
    shop: <><path d="M4 10h16v10H4Z" /><path d="m3 10 2-6h14l2 6M8 20v-6h4v6M3 10a2.5 2.5 0 0 0 5 0 2.5 2.5 0 0 0 5 0 2.5 2.5 0 0 0 5 0 2.5 2.5 0 0 0 3 0" /></>,
    hotel: <><path d="M3 20V5h12v15M3 12h18v8M7 9h.01M11 9h.01M16 16h.01" /></>,
    mic: <><rect x="9" y="3" width="6" height="11" rx="3" /><path d="M6 11a6 6 0 0 0 12 0M12 17v4M9 21h6" /></>,
    send: <><path d="m21 3-7.5 18-3.7-7.8L3 9.5Z" /><path d="M9.8 13.2 21 3" /></>,
    camera: <><rect x="3" y="6" width="18" height="14" rx="2" /><path d="m8 6 1.5-2h5L16 6" /><circle cx="12" cy="13" r="3" /></>,
    location: <><path d="M12 21s6-5.2 6-11a6 6 0 1 0-12 0c0 5.8 6 11 6 11Z" /><circle cx="12" cy="10" r="2" /></>,
    plus: <path d="M12 5v14M5 12h14" />,
    heart: <path d="M20.8 8.7c0 5.4-8.8 10.5-8.8 10.5S3.2 14.1 3.2 8.7A4.7 4.7 0 0 1 12 6.4a4.7 4.7 0 0 1 8.8 2.3Z" />,
    directions: <><path d="m3 4 7 16 3-7 7-3Z" /><path d="m13 13 7-3" /></>,
    chevron: <path d="m9 18 6-6-6-6" />,
    back: <path d="m15 18-6-6 6-6" />,
    clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
    map: <><path d="m9 18-6 3V6l6-3 6 3 6-3v15l-6 3Z" /><path d="M9 3v15M15 6v15" /></>,
    settings: <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.2 2.2-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5v.2h-3.2v-.2a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.9.3l-.1.1L6.2 17l.1-.1a1.7 1.7 0 0 0 .3-1.9 1.7 1.7 0 0 0-1.5-1H5v-3.2h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.9l-.1-.1 2.2-2.2.1.1a1.7 1.7 0 0 0 1.9.3 1.7 1.7 0 0 0 1-1.5V4h3.2v.2a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.9-.3l.1-.1 2.2 2.2-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.5 1h.1V14H20a1.7 1.7 0 0 0-1.6 1Z" /></>,
    bookmark: <path d="M6 3h12v18l-6-3.5L6 21Z" />,
    more: <><circle cx="5" cy="12" r="1" fill="currentColor" /><circle cx="12" cy="12" r="1" fill="currentColor" /><circle cx="19" cy="12" r="1" fill="currentColor" /></>,
    star: <path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9Z" />,
    sliders: <><path d="M4 7h16M4 17h16M8 7v0M16 17v0" /><circle cx="8" cy="7" r="2" /><circle cx="16" cy="17" r="2" /></>,
    zoomIn: <><circle cx="12" cy="12" r="8" /><path d="M12 8v8M8 12h8" /></>,
    zoomOut: <><circle cx="12" cy="12" r="8" /><path d="M8 12h8" /></>,
    share: <><circle cx="18" cy="5" r="2" /><circle cx="6" cy="12" r="2" /><circle cx="18" cy="19" r="2" /><path d="m8 11 8-5M8 13l8 5" /></>,
    phone: <path d="M7.5 3.5 5.7 5.3c-.7.7-.8 1.8-.3 2.7 2.2 4.3 5.7 7.8 10 10 .9.5 2 .4 2.7-.3l1.8-1.8-3.5-3.5-1.6 1c-1.5-.8-3.4-2.7-4.2-4.2l1-1.6Z" />,
    arrow: <><path d="M5 12h14" /><path d="m13 6 6 6-6 6" /></>,
  }
  return <svg {...props} aria-hidden="true">{paths[name]}</svg>
}
