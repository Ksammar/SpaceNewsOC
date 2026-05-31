import type { Category, NewsItem, NewsListResponse } from '../types/news';

const API_BASE = '/api';

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export function fetchNews(
  category?: Category,
  page: number = 1,
): Promise<NewsListResponse> {
  const params = new URLSearchParams({ page: String(page) });
  if (category) params.set('category', category);
  return fetchJson<NewsListResponse>(`${API_BASE}/news?${params}`);
}

export function fetchNewsById(id: number): Promise<NewsItem> {
  return fetchJson<NewsItem>(`${API_BASE}/news/${id}`);
}
