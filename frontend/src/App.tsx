import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchNews } from './api/client';
import Header from './components/Header';
import CategoryColumn from './components/CategoryColumn';
import type { Category, NewsItem } from './types/news';

function App() {
  const [activeCategory, setActiveCategory] = useState<Category | null>(null);

  const categories: Category[] = ['russia', 'science', 'private'];

  const queries = categories.map((cat) => ({
    category: cat,
    query: useQuery({
      queryKey: ['news', cat, 1],
      queryFn: () => fetchNews(cat),
    }),
  }));

  const allCategories = queries.map(({ category, query }) => ({
    category,
    items: query.data?.items ?? [],
    isLoading: query.isLoading,
  }));

  return (
    <div className="h-screen flex flex-col bg-space-950">
      <Header
        activeCategory={activeCategory}
        onCategoryChange={setActiveCategory}
      />

      {activeCategory ? (
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6 min-h-0">
          <div className="mb-4">
            <button
              onClick={() => setActiveCategory(null)}
              className="text-space-400 hover:text-white transition-colors text-sm"
            >
              &larr; Все категории
            </button>
          </div>
          <CategoryColumn
            category={activeCategory}
            items={queries.find((q) => q.category === activeCategory)?.query.data?.items ?? []}
            isLoading={queries.find((q) => q.category === activeCategory)?.query.isLoading ?? false}
          />
        </main>
      ) : (
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6 min-h-0">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 h-full">
            {allCategories.map(({ category, items, isLoading }) => (
              <CategoryColumn
                key={category}
                category={category}
                items={items}
                isLoading={isLoading}
              />
            ))}
          </div>
        </main>
      )}

      <footer className="border-t border-space-800 py-3 text-center text-space-400 text-xs shrink-0">
        <p>SpaceNews Aggregator &mdash; агрегатор новостей космонавтики</p>
      </footer>
    </div>
  );
}

export default App;
