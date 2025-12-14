import { useState, useEffect, useRef, memo } from "react";

/*
  Data-aware, production-ready carousel for news articles
  - Pure React (no external libs)
  - Handles missing images, long text, dynamic categories
  - Interview-grade structure (separation of concerns)
*/

function ArticleSlide({ article, category, topic }) {
  const {
    title,
    description,
    url,
    urlToImage,
    source,
    publishedAt,
  } = article;

  return (
    <article className="min-w-full h-80 grid grid-cols-2 gap-4 p-4 bg-white">
      {/* Image */}
      <div className="w-full h-full bg-gray-100 rounded-xl overflow-hidden">
        {urlToImage ? (
          <img
            src={urlToImage}
            alt={title}
            loading="lazy"
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            No image available
          </div>
        )}
      </div>

      {/* Content */}
      <div className="flex flex-col justify-between">
        <div className="space-y-2">
          <span className="text-xs font-semibold text-blue-600 uppercase">
            {category} · {topic}
          </span>

          <h2 className="text-lg font-bold line-clamp-2">{title}</h2>

          {description && (
            <p className="text-sm text-gray-600 line-clamp-3">
              {description}
            </p>
          )}
        </div>

        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>{source?.name || "Unknown source"}</span>
          <span>{new Date(publishedAt).toLocaleDateString()}</span>
        </div>

        <a
          href={url}
          target="_blank"
          rel="noreferrer"
          className="mt-3 inline-block text-sm font-semibold text-blue-600 hover:underline"
        >
          Read full article →
        </a>
      </div>
    </article>
  );
}

const MemoArticleSlide = memo(ArticleSlide);

export default function NewsCarousel({ data, autoPlay = true, interval = 4000 }) {
  /* Flatten categories → articles */
  const slides = data.flatMap((group) =>
    group.articles.map((article) => ({
      article,
      category: group.category,
      topic: group.topic,
    }))
  );

  const [current, setCurrent] = useState(0);
  const timerRef = useRef(null);
  const total = slides.length;

  const next = () => setCurrent((c) => (c + 1) % total);
  const prev = () => setCurrent((c) => (c - 1 + total) % total);

  useEffect(() => {
    if (!autoPlay || total <= 1) return;

    timerRef.current = setInterval(next, interval);
    return () => clearInterval(timerRef.current);
  }, [current, autoPlay, interval, total]);

  if (!total) return null;

  return (
    <section className="relative w-full max-w-5xl mx-auto overflow-hidden rounded-2xl shadow-xl">
      <div
        className="flex transition-transform duration-500 ease-in-out"
        style={{ transform: `translateX(-${current * 100}%)` }}
      >
        {slides.map((slide, idx) => (
          <MemoArticleSlide
            key={idx}
            article={slide.article}
            category={slide.category}
            topic={slide.topic}
          />
        ))}
      </div>

      {/* Controls */}
      <button
        onClick={prev}
        className="absolute top-1/2 left-4 -translate-y-1/2 bg-white/90 px-3 py-1 rounded-full shadow"
      >
        ‹
      </button>

      <button
        onClick={next}
        className="absolute top-1/2 right-4 -translate-y-1/2 bg-white/90 px-3 py-1 rounded-full shadow"
      >
        ›
      </button>

      {/* Indicators */}
      <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-2">
        {slides.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            className={`w-2.5 h-2.5 rounded-full ${
              i === current ? "bg-blue-600" : "bg-gray-400"
            }`}
          />
        ))}
      </div>
    </section>
  );
}
