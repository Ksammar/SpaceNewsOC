import type { NewsItem } from '../types/news';
import { CATEGORY_LABELS, CATEGORY_COLORS } from '../types/news';

interface NewsCardProps {
  news: NewsItem;
}

function timeAgo(dateStr: string | null): string {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  if (diffMins < 60) return `${diffMins} мин. назад`;
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `${diffHours} ч. назад`;
  const diffDays = Math.floor(diffHours / 24);
  if (diffDays < 7) return `${diffDays} д. назад`;
  return date.toLocaleDateString('ru-RU');
}

export default function NewsCard({ news }: NewsCardProps) {
  return (
    <a
      href={news.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block group"
    >
      <article className="card-gradient rounded-xl overflow-hidden border border-space-800/50 hover:border-space-600 transition-all duration-300 hover:shadow-lg hover:shadow-indigo-500/5 h-full flex flex-col">
        {news.image_url && (
          <div className="relative h-44 overflow-hidden">
            <img
              src={news.image_url}
              alt={news.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-space-950 via-transparent to-transparent" />
          </div>
        )}

        <div className="p-4 flex flex-col flex-1">
          <div className="flex items-center gap-2 mb-3">
            <span
              className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-medium text-white ${
                CATEGORY_COLORS[news.category]
              }`}
            >
              {CATEGORY_LABELS[news.category]}
            </span>
            {news.source_name && (
              <span className="text-xs text-space-400">{news.source_name}</span>
            )}
          </div>

          <h3 className="font-semibold text-sm leading-snug text-gray-100 group-hover:text-white transition-colors mb-2 line-clamp-3">
            {news.title_ru || news.title}
          </h3>

          {(news.summary_ru || news.summary) && (
            <p className="text-xs text-space-400 line-clamp-2 mb-3 flex-1">
              {news.summary_ru || news.summary}
            </p>
          )}

          <div className="flex items-center justify-between mt-auto pt-3 border-t border-space-800/50">
            <time className="text-xs text-space-500">
              {timeAgo(news.published_at)}
            </time>
            <span className="text-xs text-space-500 group-hover:text-space-300 transition-colors">
              Читать &rarr;
            </span>
          </div>
        </div>
      </article>
    </a>
  );
}
