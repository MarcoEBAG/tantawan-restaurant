// Mock data for Tantawan Asian Restaurant

export const menuItems = [
  // Vorspeisen
  {
    id: 1,
    category: "Vorspeisen",
    name: "Frühlingsrollen (4 Stück)",
    description: "Knusprige Frühlingsrollen mit Gemüsefüllung, serviert mit süß-sauer Sauce",
    price: 8.50,
    image: "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=300&fit=crop&crop=center"
  },
  {
    id: 2,
    category: "Vorspeisen",
    name: "Gyoza (6 Stück)",
    description: "Japanische Teigtaschen mit Schweinefleisch und Gemüse",
    price: 9.80,
    image: "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=400&h=300&fit=crop&crop=center"
  },
  {
    id: 3,
    category: "Vorspeisen",
    name: "Tom Kha Gai Suppe",
    description: "Thai Kokosnusssuppe mit Huhn, Galangal und Zitronengras",
    price: 7.90,
    image: "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=300&fit=crop&crop=center"
  },
  
  // Hauptgerichte
  {
    id: 4,
    category: "Hauptgerichte",
    name: "Pad Thai mit Huhn",
    description: "Klassische Thai-Nudeln mit Huhn, Ei, Bohnensprossen und Erdnüssen",
    price: 16.50,
    image: "https://images.unsplash.com/photo-1559847844-d2e2c6880675?w=400&h=300&fit=crop&crop=center"
  },
  {
    id: 5,
    category: "Hauptgerichte",
    name: "Sweet & Sour Schweinefleisch",
    description: "Knuspriges Schweinefleisch mit Ananas, Paprika in süß-saurer Sauce",
    price: 17.80,
    image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=center"
  },
  {
    id: 6,
    category: "Hauptgerichte",
    name: "Beef Teriyaki",
    description: "Zartes Rindfleisch in Teriyaki-Sauce mit Sesam und Frühlingszwiebeln",
    price: 19.90,
    image: "https://images.unsplash.com/photo-1534939561126-855b8675edd7?w=400&h=300&fit=crop&crop=center"
  },
  {
    id: 7,
    category: "Hauptgerichte",
    name: "Vegetarisches Curry",
    description: "Gemischtes Gemüse in cremiger Kokosmilch-Curry-Sauce",
    price: 15.50,
    image: "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400&h=300&fit=crop&crop=center"
  },
  {
    id: 8,
    category: "Hauptgerichte",
    name: "Gebratene Nudeln mit Ente",
    description: "Breite Reisnudeln mit knuspriger Ente und chinesischem Brokkoli",
    price: 21.50,
    image: "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=400&h=300&fit=crop&crop=center"
  },
  {
    id: 9,
    category: "Hauptgerichte",
    name: "Kung Pao Huhn",
    description: "Scharfes Huhn mit Erdnüssen, Chili und Szechuan-Pfefferkörner",
    price: 18.20,
    image: "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop&crop=center"
  },
  
  // Desserts
  {
    id: 10,
    category: "Desserts",
    name: "Mango Sticky Rice",
    description: "Traditioneller Thai-Dessert mit süßem Klebreis und frischer Mango",
    price: 6.50,
    image: "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop&crop=center"
  },
  {
    id: 11,
    category: "Desserts",
    name: "Sesam-Eiscreme",
    description: "Hausgemachte Eiscreme mit schwarzem Sesam",
    price: 5.50,
    image: "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=300&fit=crop&crop=center"
  }
];

export const categories = ["Vorspeisen", "Hauptgerichte", "Desserts"];

export const restaurantInfo = {
  name: "Tantawan",
  tagline: "Authentische Asiatische Küche - Günstig & Frisch",
  address: "Zürcherstrasse 232, Frauenfeld",
  phone: "+41 52 721 XX XX",
  email: "info@tantawan.ch",
  openingHours: {
    monday: "11:00 - 14:00, 17:00 - 21:30",
    tuesday: "11:00 - 14:00, 17:00 - 21:30", 
    wednesday: "11:00 - 14:00, 17:00 - 21:30",
    thursday: "11:00 - 14:00, 17:00 - 21:30",
    friday: "11:00 - 14:00, 17:00 - 22:00",
    saturday: "11:00 - 22:00",
    sunday: "17:00 - 21:30"
  }
};

export const mockOrders = [];

// Pickup time slots (next 4 hours in 15-minute intervals)
export const generatePickupTimes = () => {
  const times = [];
  const now = new Date();
  now.setMinutes(Math.ceil(now.getMinutes() / 15) * 15); // Round up to next 15 minutes
  
  for (let i = 0; i < 16; i++) { // 4 hours * 4 (15-min intervals)
    const time = new Date(now.getTime() + (i * 15 * 60 * 1000));
    times.push({
      value: time.toISOString(),
      label: time.toLocaleTimeString('de-CH', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    });
  }
  
  return times;
};