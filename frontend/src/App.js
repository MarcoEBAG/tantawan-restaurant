import React, { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "./components/ui/sonner";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Menu from "./components/Menu";
import About from "./components/About";
import Newsletter from "./components/Newsletter";
import Contact from "./components/Contact";
import Footer from "./components/Footer";
import Cart from "./components/Cart";

function App() {
  const [cartItems, setCartItems] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  const handleAddToCart = (item) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(cartItem => cartItem.id === item.id);
      
      if (existingItem) {
        if (item.quantity && item.quantity < 0) {
          // Remove item or decrease quantity
          const newQuantity = existingItem.quantity + item.quantity;
          if (newQuantity <= 0) {
            return prevItems.filter(cartItem => cartItem.id !== item.id);
          } else {
            return prevItems.map(cartItem =>
              cartItem.id === item.id 
                ? { ...cartItem, quantity: newQuantity }
                : cartItem
            );
          }
        } else {
          // Increase quantity
          return prevItems.map(cartItem =>
            cartItem.id === item.id 
              ? { ...cartItem, quantity: cartItem.quantity + 1 }
              : cartItem
          );
        }
      } else {
        // Add new item
        return [...prevItems, { ...item, quantity: 1 }];
      }
    });
  };

  const handleUpdateCart = (item) => {
    handleAddToCart(item);
  };

  const handleClearCart = () => {
    setCartItems([]);
  };

  return (
    <div className="App">
      <BrowserRouter>
        <Header 
          cartItems={cartItems} 
          onCartOpen={() => setIsCartOpen(true)} 
        />
        
        <Routes>
          <Route path="/" element={
            <main>
              <Hero />
              <Menu 
                onAddToCart={handleAddToCart} 
                cartItems={cartItems}
              />
              <About />
              <Newsletter />
              <Contact />
            </main>
          } />
        </Routes>

        <Footer />

        <Cart
          isOpen={isCartOpen}
          onClose={() => setIsCartOpen(false)}
          cartItems={cartItems}
          onUpdateCart={handleUpdateCart}
          onClearCart={handleClearCart}
        />

        <Toaster position="top-right" />
      </BrowserRouter>
    </div>
  );
}

export default App;