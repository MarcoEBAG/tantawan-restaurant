import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Sheet, SheetContent, SheetHeader, SheetTitle } from './ui/sheet';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Textarea } from './ui/textarea';
import { Separator } from './ui/separator';
import { Plus, Minus, Trash2, Clock, User, Phone, MessageSquare, Loader2, CheckCircle } from 'lucide-react';
import { generatePickupTimes } from '../data/mockData';
import { ordersAPI } from '../services/api';
import { toast } from 'sonner';

const Cart = ({ isOpen, onClose, cartItems, onUpdateCart, onClearCart }) => {
  const [customerInfo, setCustomerInfo] = useState({
    name: '',
    phone: '',
    pickupTime: '',
    notes: ''
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [orderSuccess, setOrderSuccess] = useState(null);
  
  const pickupTimes = generatePickupTimes();
  
  const total = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const itemCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  const handleQuantityChange = (item, change) => {
    onUpdateCart({ ...item, quantity: change });
  };

  const handleRemoveItem = (itemId) => {
    const item = cartItems.find(item => item.id === itemId);
    if (item) {
      onUpdateCart({ ...item, quantity: -item.quantity });
    }
  };

  const validateForm = () => {
    if (!customerInfo.name.trim()) {
      toast.error('Bitte geben Sie Ihren Namen ein');
      return false;
    }
    
    if (!customerInfo.phone.trim()) {
      toast.error('Bitte geben Sie Ihre Telefonnummer ein');
      return false;
    }
    
    if (!customerInfo.pickupTime) {
      toast.error('Bitte wählen Sie eine Abholzeit');
      return false;
    }
    
    if (cartItems.length === 0) {
      toast.error('Ihr Warenkorb ist leer');
      return false;
    }
    
    return true;
  };

  const handleOrderSubmit = async () => {
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    
    try {
      // Prepare order data for API
      const orderData = {
        items: cartItems.map(item => ({
          menu_item_id: item.id,
          name: item.name,
          price: item.price,
          quantity: item.quantity
        })),
        customer: {
          name: customerInfo.name.trim(),
          phone: customerInfo.phone.trim(),
          notes: customerInfo.notes.trim() || undefined
        },
        pickup_time: new Date(customerInfo.pickupTime).toISOString()
      };

      console.log('Submitting order:', orderData);
      
      // Submit order to API
      const order = await ordersAPI.createOrder(orderData);
      
      console.log('Order created successfully:', order);
      
      // Show success state
      setOrderSuccess(order);
      
      // Show success toast
      const pickupTimeLabel = pickupTimes.find(t => t.value === customerInfo.pickupTime)?.label || 'gewählte Zeit';
      toast.success(`Bestellung erfolgreich aufgegeben! Bestellnummer: ${order.order_number}`);
      
      // Reset form and cart after short delay
      setTimeout(() => {
        setCustomerInfo({ name: '', phone: '', pickupTime: '', notes: '' });
        onClearCart();
        setOrderSuccess(null);
        onClose();
      }, 5000);
      
    } catch (error) {
      console.error('Order submission failed:', error);
      toast.error(error.message || 'Bestellung fehlgeschlagen. Bitte versuchen Sie es erneut.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Success state
  if (orderSuccess) {
    return (
      <Sheet open={isOpen} onOpenChange={onClose}>
        <SheetContent side="right" className="w-full sm:max-w-lg overflow-y-auto">
          <SheetHeader>
            <SheetTitle className="text-2xl font-bold text-green-600">Bestellung Erfolgreich!</SheetTitle>
          </SheetHeader>

          <div className="space-y-6 mt-6">
            <Card className="border-green-200 bg-green-50">
              <CardContent className="p-6 text-center">
                <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-4" />
                
                <h3 className="text-xl font-semibold text-green-800 mb-2">
                  Ihre Bestellung wurde aufgegeben!
                </h3>
                
                <div className="bg-white rounded-lg p-4 mb-4">
                  <p className="text-sm text-gray-600 mb-1">Bestellnummer</p>
                  <p className="text-2xl font-bold text-black">{orderSuccess.order_number}</p>
                </div>
                
                <div className="space-y-2 text-sm text-green-700 mb-4">
                  <p><strong>Name:</strong> {orderSuccess.customer.name}</p>
                  <p><strong>Telefon:</strong> {orderSuccess.customer.phone}</p>
                  <p><strong>Abholzeit:</strong> {new Date(orderSuccess.pickup_time).toLocaleString('de-CH')}</p>
                  <p><strong>Gesamt:</strong> CHF {orderSuccess.total.toFixed(2)}</p>
                </div>
                
                <div className="bg-[#ECEC75] rounded-lg p-4 mb-4">
                  <p className="text-sm font-semibold text-black mb-1">
                    📍 Abholung bei Tantawan
                  </p>
                  <p className="text-xs text-gray-700">
                    Zürcherstrasse 232, Frauenfeld
                  </p>
                </div>
                
                <p className="text-xs text-gray-600 leading-relaxed">
                  Sie erhalten eine Bestätigung per Telefon. Bei Fragen rufen Sie uns gerne an.
                  Dieses Fenster schließt sich automatisch in wenigen Sekunden.
                </p>
              </CardContent>
            </Card>
          </div>
        </SheetContent>
      </Sheet>
    );
  }

  return (
    <Sheet open={isOpen} onOpenChange={onClose}>
      <SheetContent side="right" className="w-full sm:max-w-lg overflow-y-auto">
        <SheetHeader>
          <SheetTitle className="text-2xl font-bold">Warenkorb</SheetTitle>
        </SheetHeader>

        <div className="space-y-6 mt-6">
          {/* Cart Items */}
          {cartItems.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">Ihr Warenkorb ist leer</p>
              <Button variant="outline" onClick={onClose} className="mt-4">
                Zurück zur Speisekarte
              </Button>
            </div>
          ) : (
            <>
              <div className="space-y-4">
                {cartItems.map((item) => (
                  <Card key={item.id} className="border-gray-200">
                    <CardContent className="p-4">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h4 className="font-semibold text-black">{item.name}</h4>
                          <p className="text-sm text-gray-600 mt-1">CHF {item.price.toFixed(2)}</p>
                        </div>
                        
                        <div className="flex items-center space-x-2 ml-4">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleQuantityChange(item, -1)}
                            className="h-8 w-8 p-0"
                            disabled={isSubmitting}
                          >
                            <Minus className="h-4 w-4" />
                          </Button>
                          <span className="font-semibold min-w-[2rem] text-center">
                            {item.quantity}
                          </span>
                          <Button
                            size="sm"
                            onClick={() => handleQuantityChange(item, 1)}
                            className="h-8 w-8 p-0 bg-black text-white hover:bg-gray-800"
                            disabled={isSubmitting}
                          >
                            <Plus className="h-4 w-4" />
                          </Button>
                          <Button
                            size="sm"
                            variant="destructive"
                            onClick={() => handleRemoveItem(item.id)}
                            className="h-8 w-8 p-0 ml-2"
                            disabled={isSubmitting}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                      
                      <div className="flex justify-between items-center mt-3 pt-3 border-t">
                        <span className="text-sm text-gray-600">Zwischensumme:</span>
                        <span className="font-semibold">CHF {(item.price * item.quantity).toFixed(2)}</span>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              <Separator />

              {/* Order Summary */}
              <Card className="bg-[#ECEC75] border-0">
                <CardContent className="p-4">
                  <div className="flex justify-between items-center text-lg font-bold">
                    <span>Gesamt ({itemCount} Artikel):</span>
                    <span>CHF {total.toFixed(2)}</span>
                  </div>
                </CardContent>
              </Card>

              {/* Customer Information */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg flex items-center">
                    <User className="h-5 w-5 mr-2" />
                    Bestellinformationen
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">Name *</Label>
                    <Input
                      id="name"
                      placeholder="Ihr Name"
                      value={customerInfo.name}
                      onChange={(e) => setCustomerInfo(prev => ({ ...prev, name: e.target.value }))}
                      disabled={isSubmitting}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="phone">Telefon *</Label>
                    <Input
                      id="phone"
                      placeholder="+41 52 XXX XX XX"
                      value={customerInfo.phone}
                      onChange={(e) => setCustomerInfo(prev => ({ ...prev, phone: e.target.value }))}
                      disabled={isSubmitting}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label>Abholzeit *</Label>
                    <Select 
                      value={customerInfo.pickupTime} 
                      onValueChange={(value) => setCustomerInfo(prev => ({ ...prev, pickupTime: value }))}
                      disabled={isSubmitting}
                    >
                      <SelectTrigger>
                        <div className="flex items-center">
                          <Clock className="h-4 w-4 mr-2" />
                          <SelectValue placeholder="Wählen Sie eine Zeit" />
                        </div>
                      </SelectTrigger>
                      <SelectContent>
                        {pickupTimes.map((time) => (
                          <SelectItem key={time.value} value={time.value}>
                            {time.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="notes">Notizen (optional)</Label>
                    <Textarea
                      id="notes"
                      placeholder="Besondere Wünsche oder Anmerkungen..."
                      value={customerInfo.notes}
                      onChange={(e) => setCustomerInfo(prev => ({ ...prev, notes: e.target.value }))}
                      rows={3}
                      disabled={isSubmitting}
                    />
                  </div>
                </CardContent>
              </Card>

              {/* Order Button */}
              <Button
                onClick={handleOrderSubmit}
                className="w-full bg-black text-white hover:bg-gray-800 text-lg py-6 font-semibold"
                disabled={isSubmitting || !customerInfo.name || !customerInfo.phone || !customerInfo.pickupTime}
              >
                {isSubmitting ? (
                  <div className="flex items-center justify-center">
                    <Loader2 className="h-5 w-5 animate-spin mr-2" />
                    Bestellung wird aufgegeben...
                  </div>
                ) : (
                  `Bestellung Aufgeben - CHF ${total.toFixed(2)}`
                )}
              </Button>

              <div className="text-xs text-gray-500 text-center">
                * Pflichtfelder müssen ausgefüllt werden
              </div>
            </>
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
};

export default Cart;