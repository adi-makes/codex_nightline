import { Icon } from './Icon'
import type { Route } from '../App'

const items: { route: Route; label: string; icon: 'home' | 'search' | 'bag' | 'user' }[] = [
  { route: '/', label: 'Home', icon: 'home' }, { route: '/explore', label: 'Explore', icon: 'search' }, { route: '/trips', label: 'Trips', icon: 'bag' }, { route: '/profile', label: 'Profile', icon: 'user' },
]

export function BottomNav({ route, navigate }: { route: Route; navigate: (route: Route) => void }) {
  return <nav className="bottom-nav" aria-label="Primary navigation">
    {items.slice(0, 2).map((item) => <button className={route === item.route ? 'active' : ''} key={item.route} onClick={() => navigate(item.route)}><Icon name={item.icon} /><span>{item.label}</span></button>)}
    <button className="ask-fab" aria-label="Ask Kochi" onClick={() => navigate('/ask')}><b><Icon name="sparkles" size={24} /></b><span>Ask</span></button>
    {items.slice(2).map((item) => <button className={route === item.route ? 'active' : ''} key={item.route} onClick={() => navigate(item.route)}><Icon name={item.icon} /><span>{item.label}</span></button>)}
  </nav>
}
