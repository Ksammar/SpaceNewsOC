import type { Category } from '../types/news';
import { CATEGORY_LABELS } from '../types/news';

interface HeaderProps {
  activeCategory: Category | null;
  onCategoryChange: (category: Category | null) => void;
}

const categories: Category[] = ['russia', 'science', 'private'];

const categoryIcons: Record<Category, string> = {
  russia: '🛰️',
  science: '🔭',
  private: '🚀',
};

export default function Header({ activeCategory, onCategoryChange }: HeaderProps) {
  return (
    <header className="border-b border-space-800 bg-space-900/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <button
            onClick={() => onCategoryChange(null)}
            className="flex items-center gap-3 group"
          >
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-500 flex items-center justify-center text-lg">
              ✦
            </div>
            <div>
              <h1 className="text-xl font-bold text-white group-hover:text-space-300 transition-colors">
                SpaceNews
              </h1>
              <p className="text-xs text-space-400 hidden sm:block">
                Агрегатор новостей космонавтики
              </p>
            </div>
          </button>

          <nav className="flex gap-2">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() =>
                  onCategoryChange(activeCategory === cat ? null : cat)
                }
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeCategory === cat
                    ? 'bg-space-700 text-white ring-1 ring-space-500'
                    : 'text-space-300 hover:text-white hover:bg-space-800'
                }`}
              >
                <span className="mr-1.5">{categoryIcons[cat]}</span>
                {CATEGORY_LABELS[cat]}
              </button>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
}
