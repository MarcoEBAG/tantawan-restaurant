import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  Search, 
  Refresh,
  Phone,
  Calendar,
  DollarSign,
  ShoppingBag,
  User,
  Printer,
  Trash2
} from 'lucide-react';
import { adminAPI } from '../services/api';
import { toast } from 'sonner';

const AdminDashboard = () => {
  const [orders, setOrders] = useState([]);
  const [pendingOrders, setPendingOrders] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [refreshInterval, setRefreshInterval] = useState(null);

  // Order status configurations
  const statusConfig = {
    pending: { label: 'Wartend', color: 'bg-yellow-500', textColor: 'text-yellow-700', bgColor: 'bg-yellow-50' },
    confirmed: { label: 'Bestätigt', color: 'bg-blue-500', textColor: 'text-blue-700', bgColor: 'bg-blue-50' },
    preparing: { label: 'In Zubereitung', color: 'bg-orange-500', textColor: 'text-orange-700', bgColor: 'bg-orange-50' },
    ready: { label: 'Bereit', color: 'bg-green-500', textColor: 'text-green-700', bgColor: 'bg-green-50' },
    completed: { label: 'Abgeholt', color: 'bg-gray-500', textColor: 'text-gray-700', bgColor: 'bg-gray-50' },
    cancelled: { label: 'Storniert', color: 'bg-red-500', textColor: 'text-red-700', bgColor: 'bg-red-50' }
  };

  // Fetch initial data
  useEffect(() => {
    fetchDashboardData();
    
    // Set up auto-refresh every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    setRefreshInterval(interval);
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [ordersData, pendingData, statsData] = await Promise.all([
        adminAPI.getTodaysOrders(),
        adminAPI.getPendingOrders(),
        adminAPI.getOrderStats()
      ]);
      
      setOrders(ordersData);
      setPendingOrders(pendingData);
      setStats(statsData);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Fehler beim Laden der Dashboard-Daten');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (orderId, newStatus) => {
    try {
      await adminAPI.updateOrderStatus(orderId, newStatus);
      toast.success('Bestellstatus erfolgreich aktualisiert');
      fetchDashboardData(); // Refresh data
    } catch (error) {
      console.error('Error updating order status:', error);
      toast.error('Fehler beim Aktualisieren des Bestellstatus');
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchDashboardData();
      return;
    }

    try {
      const searchResults = await adminAPI.searchOrders(searchQuery);
      setOrders(searchResults);
    } catch (error) {
      console.error('Error searching orders:', error);
      toast.error('Fehler bei der Suche');
    }
  };

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString('de-CH', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('de-CH');
  };

  const getNextStatus = (currentStatus) => {
    const statusFlow = {
      'pending': 'confirmed',
      'confirmed': 'preparing',
      'preparing': 'ready',
      'ready': 'completed'
    };
    return statusFlow[currentStatus];
  };

  const OrderCard = ({ order, showActions = true }) => {
    const config = statusConfig[order.status] || statusConfig.pending;
    const nextStatus = getNextStatus(order.status);
    
    return (
      <Card className={`border-l-4 border-l-${config.color.replace('bg-', '')} ${config.bgColor} mb-4`}>
        <CardHeader className="pb-3">
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-lg font-bold">{order.order_number}</CardTitle>
              <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                <span className="flex items-center">
                  <User className="h-4 w-4 mr-1" />
                  {order.customer.name}
                </span>
                <span className="flex items-center">
                  <Phone className="h-4 w-4 mr-1" />
                  {order.customer.phone}
                </span>
                <span className="flex items-center">
                  <Clock className="h-4 w-4 mr-1" />
                  {formatTime(order.pickup_time)}
                </span>
              </div>
            </div>
            <Badge className={`${config.color} text-white`}>
              {config.label}
            </Badge>
          </div>
        </CardHeader>
        
        <CardContent>
          {/* Order Items */}
          <div className="space-y-2 mb-4">
            {order.items.map((item, index) => (
              <div key={index} className="flex justify-between items-center text-sm">
                <span>{item.quantity}x {item.name}</span>
                <span className="font-medium">CHF {(item.price * item.quantity).toFixed(2)}</span>
              </div>
            ))}
            <div className="border-t pt-2 flex justify-between items-center font-bold">
              <span>Gesamt:</span>
              <span>CHF {order.total.toFixed(2)}</span>
            </div>
          </div>

          {/* Notes */}
          {order.customer.notes && (
            <div className="bg-yellow-50 border border-yellow-200 rounded p-3 mb-4">
              <p className="text-sm text-yellow-800">
                <strong>Notizen:</strong> {order.customer.notes}
              </p>
            </div>
          )}

          {/* Actions */}
          {showActions && (
            <div className="flex gap-2 flex-wrap">
              {nextStatus && (
                <Button
                  size="sm"
                  onClick={() => handleStatusUpdate(order.id, nextStatus)}
                  className="bg-green-600 hover:bg-green-700 text-white"
                >
                  <CheckCircle className="h-4 w-4 mr-1" />
                  {statusConfig[nextStatus].label}
                </Button>
              )}
              
              {order.status !== 'completed' && order.status !== 'cancelled' && (
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => handleStatusUpdate(order.id, 'cancelled')}
                  className="border-red-300 text-red-600 hover:bg-red-50"
                >
                  <AlertCircle className="h-4 w-4 mr-1" />
                  Stornieren
                </Button>
              )}
              
              <Button
                size="sm"
                variant="outline"
                onClick={() => window.print()}
                className="border-gray-300"
              >
                <Printer className="h-4 w-4 mr-1" />
                Drucken
              </Button>
            </div>
          )}
          
          <div className="text-xs text-gray-500 mt-3 pt-3 border-t">
            Bestellt: {formatDate(order.created_at)} um {formatTime(order.created_at)}
          </div>
        </CardContent>
      </Card>
    );
  };

  if (loading && !stats) {
    return (
      <div className="p-8">
        <div className="flex justify-center items-center min-h-[400px]">
          <div className="text-center">
            <div className="loading-spinner mx-auto mb-4" />
            <p className="text-lg text-gray-600">Dashboard wird geladen...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-3xl font-bold text-black" style={{ fontFamily: 'var(--font-serif)' }}>
              🍜 Tantawan Admin Dashboard
            </h1>
            <Button onClick={fetchDashboardData} disabled={loading}>
              <Refresh className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              Aktualisieren
            </Button>
          </div>

          {/* Stats Cards */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Heute Bestellungen</p>
                      <p className="text-2xl font-bold">{stats.today.orders}</p>
                    </div>
                    <ShoppingBag className="h-8 w-8 text-blue-500" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Heute Umsatz</p>
                      <p className="text-2xl font-bold">CHF {stats.today.revenue}</p>
                    </div>
                    <DollarSign className="h-8 w-8 text-green-500" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Offene Bestellungen</p>
                      <p className="text-2xl font-bold">{stats.pending_orders}</p>
                    </div>
                    <Clock className="h-8 w-8 text-orange-500" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Letzte Aktualisierung</p>
                      <p className="text-sm font-medium">{formatTime(stats.timestamp)}</p>
                    </div>
                    <Calendar className="h-8 w-8 text-purple-500" />
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>

        {/* Main Content */}
        <Tabs defaultValue="pending" className="space-y-6">
          <TabsList className="grid grid-cols-3 w-full max-w-md">
            <TabsTrigger value="pending">Küche ({pendingOrders.length})</TabsTrigger>
            <TabsTrigger value="today">Heute ({orders.length})</TabsTrigger>
            <TabsTrigger value="search">Suche</TabsTrigger>
          </TabsList>

          {/* Pending Orders - Kitchen View */}
          <TabsContent value="pending">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Clock className="h-5 w-5 mr-2 text-orange-500" />
                  Küchen-Übersicht - Offene Bestellungen
                </CardTitle>
              </CardHeader>
              <CardContent>
                {pendingOrders.length === 0 ? (
                  <div className="text-center py-8">
                    <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
                    <p className="text-lg text-gray-600">Keine offenen Bestellungen! 🎉</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    {pendingOrders.map(order => (
                      <OrderCard key={order.id} order={order} />
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Today's Orders */}
          <TabsContent value="today">
            <Card>
              <CardHeader>
                <CardTitle>Heutige Bestellungen</CardTitle>
              </CardHeader>
              <CardContent>
                {orders.length === 0 ? (
                  <div className="text-center py-8">
                    <ShoppingBag className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-lg text-gray-600">Noch keine Bestellungen heute.</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {orders.map(order => (
                      <OrderCard key={order.id} order={order} showActions={false} />
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Search */}
          <TabsContent value="search">
            <Card>
              <CardHeader>
                <CardTitle>Bestellungen Suchen</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4 mb-6">
                  <div className="flex-1">
                    <Input
                      placeholder="Bestellnummer, Kundenname oder Telefon..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                    />
                  </div>
                  <Button onClick={handleSearch}>
                    <Search className="h-4 w-4 mr-2" />
                    Suchen
                  </Button>
                </div>

                {orders.length > 0 && (
                  <div className="space-y-4">
                    {orders.map(order => (
                      <OrderCard key={order.id} order={order} showActions={false} />
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AdminDashboard;