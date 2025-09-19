import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Plus, Minus, Loader2, AlertCircle } from 'lucide-react';
import { menuAPI } from '../services/api';
import { toast } from 'sonner';

const Menu = ({ onAddToCart, cartItems = [] }) => {
  const [selectedCategory, setSelectedCategory] = useState('Vorspeisen');
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const categories = ['Vorspeisen', 'Hauptgerichte', 'Desserts'];

  // Fetch menu items on component mount
  useEffect(() => {
    const fetchMenuItems = async () => {
      try {
        setLoading(true);
        setError(null);
        const items = await menuAPI.getAllItems();
        setMenuItems(items);
      } catch (err) {
        console.error('Error fetching menu items:', err);
        setError(err.message);
        toast.error('Fehler beim Laden der Speisekarte');
      } finally {
        setLoading(false);
      }
    };

    fetchMenuItems();
  }, []);

  const getCartQuantity = (itemId) => {
    const cartItem = cartItems.find(item => item.id === itemId);
    return cartItem ? cartItem.quantity : 0;
  };

  const handleAddToCart = (item) => {
    onAddToCart(item);
  };

  const filteredItems = menuItems.filter(item => item.category === selectedCategory);

  // Loading state
  if (loading) {
    return (
      <section id="menu" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
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

          <div className="flex justify-center items-center py-20">
            <div className="text-center">
              <Loader2 className="h-12 w-12 animate-spin text-black mx-auto mb-4" />
              <p className="text-lg text-gray-600">Speisekarte wird geladen...</p>
            </div>
          </div>
        </div>
      </section>
    );
  }

  // Error state
  if (error) {
    return (
      <section id="menu" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 
              className="text-4xl md:text-5xl font-bold text-black mb-4"
              style={{ fontFamily: 'var(--font-serif)' }}
            >
              Unsere Speisekarte
            </h2>
          </div>

          <div className="flex justify-center items-center py-20">
            <Card className="border-red-200 bg-red-50 max-w-md">
              <CardContent className="p-8 text-center">
                <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-red-800 mb-2">
                  Fehler beim Laden der Speisekarte
                </h3>
                <p className="text-red-600 mb-4">{error}</p>
                <Button 
                  onClick={() => window.location.reload()}
                  className="bg-red-600 hover:bg-red-700 text-white"
                >
                  Seite neu laden
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    );
  }

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
              <Badge variant="secondary" className="ml-2 bg-gray-200 text-gray-700">
                {menuItems.filter(item => item.category === category).length}
              </Badge>
            </Button>
          ))}
        </div>

        {/* Menu Grid */}
        {filteredItems.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-lg text-gray-500">
              Keine Gerichte in der Kategorie "{selectedCategory}" verfügbar.
            </p>
          </div>
        ) : (
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
                      onError={(e) => {
                        e.target.src = 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop&crop=center';
                      }}
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
        )}
      </div>
    </section>
  );
};

export default Menu;