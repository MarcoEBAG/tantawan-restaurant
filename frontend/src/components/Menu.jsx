import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Plus, Minus } from 'lucide-react';
import { menuItems, categories } from '../data/mockData';

const Menu = ({ onAddToCart, cartItems = [] }) => {
  const [selectedCategory, setSelectedCategory] = useState('Vorspeisen');

  const getCartQuantity = (itemId) => {
    const cartItem = cartItems.find(item => item.id === itemId);
    return cartItem ? cartItem.quantity : 0;
  };

  const handleAddToCart = (item) => {
    onAddToCart(item);
  };

  const filteredItems = menuItems.filter(item => item.category === selectedCategory);

  return (
    <section id="menu" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 
            className="text-4xl md:text-5xl font-bold text-black mb-4"
            style={{ fontFamily: 'var(--font-serif)' }}
          >
            Unsere Speisekarte
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Entdecken Sie unsere Auswahl an frisch zubereiteten asiatischen Gerichten. 
            Alle Preise verstehen sich für Takeaway.
          </p>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {categories.map((category) => (
            <Button
              key={category}
              variant={selectedCategory === category ? "default" : "outline"}
              onClick={() => setSelectedCategory(category)}
              className={`px-6 py-3 font-semibold transition-all duration-200 ${
                selectedCategory === category
                  ? 'bg-black text-white hover:bg-gray-800'
                  : 'border-black text-black hover:bg-black hover:text-white'
              }`}
            >
              {category}
            </Button>
          ))}
        </div>

        {/* Menu Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredItems.map((item) => {
            const quantity = getCartQuantity(item.id);
            
            return (
              <Card key={item.id} className="group hover:shadow-xl transition-all duration-300 border-0 bg-white rounded-2xl overflow-hidden">
                <div className="relative">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute top-4 right-4">
                    <Badge className="bg-[#ECEC75] text-black font-semibold">
                      CHF {item.price.toFixed(2)}
                    </Badge>
                  </div>
                </div>
                
                <CardContent className="p-6">
                  <div className="space-y-3">
                    <h3 className="text-xl font-bold text-black">{item.name}</h3>
                    <p className="text-gray-600 text-sm leading-relaxed">{item.description}</p>
                    
                    <div className="flex items-center justify-between pt-4">
                      <div className="text-lg font-bold text-black">
                        CHF {item.price.toFixed(2)}
                      </div>
                      
                      {quantity === 0 ? (
                        <Button
                          onClick={() => handleAddToCart(item)}
                          className="bg-black text-white hover:bg-gray-800 transition-all duration-200 hover:transform hover:-translate-y-0.5"
                        >
                          <Plus className="h-4 w-4 mr-2" />
                          Hinzufügen
                        </Button>
                      ) : (
                        <div className="flex items-center space-x-3">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => onAddToCart({ ...item, quantity: -1 })}
                            className="border-black text-black hover:bg-black hover:text-white h-8 w-8 p-0"
                          >
                            <Minus className="h-4 w-4" />
                          </Button>
                          <span className="font-semibold text-lg min-w-[2rem] text-center">
                            {quantity}
                          </span>
                          <Button
                            size="sm"
                            onClick={() => handleAddToCart(item)}
                            className="bg-black text-white hover:bg-gray-800 h-8 w-8 p-0"
                          >
                            <Plus className="h-4 w-4" />
                          </Button>
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Menu;