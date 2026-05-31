import type { Category, NewsItem } from '../types/news';
import { CATEGORY_LABELS } from '../types/news';
import NewsCard from './NewsCard';

interface CategoryColumnProps {
  category: Category;
  items: NewsItem[];
  isLoading: boolean;
}

const columnGradients: Record<Category, string> = {
  russia: 'from-indigo-500/10 via-transparent to-transparent',
  science: 'from-cyan-500/10 via-transparent to-transparent',
  private: 'from-amber-500/10 via-transparent to-transparent',
};

const columnBorders: Record<Category, string> = {
  russia: 'border-indigo-500/20',
  science: 'border-cyan-500/20',
  private: 'border-amber-500/20',
};

export default function CategoryColumn({
  category,
  items,
  isLoading,
}: CategoryColumnProps) {
  return (
    <section
      className={`rounded-2xl border bg-gradient-to-b ${columnGradients[category]} ${columnBorders[category]} p-5 flex flex-col min-h-0`}
    >
      <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2 shrink-0">
        <span
          className={`w-2 h-2 rounded-full ${
            category === 'russia'
              ? 'bg-indigo-500'
              : category === 'science'
                ? 'bg-cyan-500'
                : 'bg-amber-500'
          }`}
        />
        {CATEGORY_LABELS[category]}
        {!isLoading && (
          <span className="text-xs font-normal text-space-400 ml-auto">
            {items.length} новостей
          </span>
        )}
      </h2>

      <div className="flex-1 overflow-y-auto min-h-0 space-y-4 pr-1 -mr-1">
        {isLoading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div
                key={i}
                className="animate-pulse rounded-xl bg-space-800/50 h-48"
              />
            ))}
          </div>
        ) : items.length === 0 ? (
          <p className="text-space-500 text-sm text-center py-8">
            Новостей пока нет
          </p>
        ) : (
          items.slice(0, 20).map((news) => (
            <NewsCard key={news.id} news={news} />
          ))
        )}
      </div>
    </section>
  );
}
