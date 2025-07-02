import React, { createContext, useState, useEffect } from 'react';

export const FavouriteContext = createContext();

export const FavouriteProvider = ({ children }) => {
  const [favourites, setFavourites] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem('favourites');
    if (saved) setFavourites(JSON.parse(saved));
  }, []);

  useEffect(() => {
    localStorage.setItem('favourites', JSON.stringify(favourites));
  }, [favourites]);

  const addFavourite = (item) => {
    setFavourites((prev) => [...prev, item]);
  };

  const removeFavourite = (id) => {
    setFavourites((prev) => prev.filter((item) => item.id !== id));
  };

  return (
    <FavouriteContext.Provider value={{ favourites, addFavourite, removeFavourite }}>
      {children}
    </FavouriteContext.Provider>
  );
};


import React, { createContext, useState, useEffect } from 'react';

export const FavouriteContext = createContext();

export const FavouriteProvider = ({ children }) => {
  const [favourites, setFavourites] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem('favourites');
    if (saved) setFavourites(JSON.parse(saved));
  }, []);

  useEffect(() => {
    localStorage.setItem('favourites', JSON.stringify(favourites));
  }, [favourites]);

  const addFavourite = (item) => {
    setFavourites((prev) => [...prev, item]);
  };

  const removeFavourite = (id) => {
    setFavourites((prev) => prev.filter((item) => item.id !== id));
  };

  return (
    <FavouriteContext.Provider value={{ favourites, addFavourite, removeFavourite }}>
      {children}
    </FavouriteContext.Provider>
  );
};

const ProductCard = React.memo(({ product, onClick }) => {
  return (
    <div>
      <h4>{product.name}</h4>
      <button onClick={() => onClick(product.id)}>Добавить</button>
    </div>
  );
});
import { Suspense, lazy } from 'react';

const FavouritesPage = lazy(() => import('./pages/FavouritesPage'));

<Route
  path="/favourites"
  element={
    <Suspense fallback={<div>Загрузка...</div>}>
      <FavouritesPage />
    </Suspense>
  }
/>
import { render, screen } from '@testing-library/react';
import { FavouritesPage } from '../pages/FavouritesPage';
import { FavouriteContext } from '../context/FavouriteContext';

test('renders favourites list', () => {
  render(
    <FavouriteContext.Provider value={{ favourites: [{ id: 1, name: 'Товар', quantity: 1 }], removeFavourite: jest.fn() }}>
      <FavouritesPage />
    </FavouriteContext.Provider>
  );

  expect(screen.getByText(/Избранное/i)).toBeInTheDocument();
  expect(screen.getByText(/Товар/i)).toBeInTheDocument();
});
