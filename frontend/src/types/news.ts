export type Category = 'russia' | 'science' | 'private';

export interface NewsItem {
  id: number;
  title: string;
  url: string;
  summary: string | null;
  title_ru: string | null;
  summary_ru: string | null;
  image_url: string | null;
  published_at: string | null;
  category: Category;
  source_name: string | null;
  created_at: string;
}

export interface NewsDetail extends NewsItem {
  content: string | null;
}

export interface NewsListResponse {
  items: NewsItem[];
  total: number;
  page: number;
  pages: number;
}

export const CATEGORY_LABELS: Record<Category, string> = {
  russia: 'Россия',
  science: 'Наука',
  private: 'Частный космос',
};

export const CATEGORY_COLORS: Record<Category, string> = {
  russia: 'bg-indigo-500',
  science: 'bg-cyan-500',
  private: 'bg-amber-500',
};
