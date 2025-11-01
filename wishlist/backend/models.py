import os
import yaml
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from config import Config

class WishlistItem:
    """Represents a single wishlist item."""
    
    def __init__(self, title: str, image: str = None, weblink: str = None, item_id: str = None, order: int = None, deleted: str = None):
        self.id = item_id or str(uuid.uuid4())
        self.title = title
        self.image = image  # filename of the uploaded image
        self.weblink = weblink
        self.order = order if order is not None else 0
        self.created_at = datetime.now().isoformat()
        self.deleted = deleted  # timestamp when item was deleted, None if not deleted
    
    def to_dict(self) -> Dict:
        """Convert the item to a dictionary for YAML serialization."""
        data = {
            'id': self.id,
            'title': self.title,
            'image': self.image,
            'weblink': self.weblink,
            'order': self.order,
            'created_at': self.created_at
        }
        # Only include deleted field if it exists
        if self.deleted:
            data['deleted'] = self.deleted
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'WishlistItem':
        """Create a WishlistItem from a dictionary."""
        item = cls(
            title=data['title'],
            image=data.get('image'),
            weblink=data.get('weblink'),
            item_id=data.get('id'),
            order=data.get('order', 0),
            deleted=data.get('deleted')
        )
        item.created_at = data.get('created_at', datetime.now().isoformat())
        return item

class MultiWishlistManager:
    """Manages multiple wishlists with tabs for different kids."""
    
    def __init__(self):
        Config.ensure_directories()
        self.tabs_config_path = os.path.join(Config.DATA_FOLDER, 'tabs.yaml')
        self._ensure_tabs_config()
    
    def _ensure_tabs_config(self):
        """Create tabs configuration file if it doesn't exist."""
        if not os.path.exists(self.tabs_config_path):
            default_tabs = [
                {
                    'id': str(uuid.uuid4()),
                    'name': 'My Wishlist',
                    'filename': 'wishlist.yaml',
                    'created_at': datetime.now().isoformat()
                }
            ]
            with open(self.tabs_config_path, 'w') as f:
                yaml.safe_dump(default_tabs, f)
    
    def get_tabs(self) -> List[Dict]:
        """Get list of all wishlist tabs."""
        try:
            with open(self.tabs_config_path, 'r') as f:
                return yaml.safe_load(f) or []
        except Exception as e:
            print(f"Error loading tabs: {e}")
            return []
    
    def save_tabs(self, tabs: List[Dict]):
        """Save tabs configuration."""
        try:
            with open(self.tabs_config_path, 'w') as f:
                yaml.safe_dump(tabs, f, default_flow_style=False)
        except Exception as e:
            print(f"Error saving tabs: {e}")
            raise
    
    def create_tab(self, name: str) -> Dict:
        """Create a new wishlist tab."""
        tabs = self.get_tabs()
        
        # Generate unique filename
        safe_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name.lower())
        filename = f"wishlist_{safe_name}_{str(uuid.uuid4())[:8]}.yaml"
        
        new_tab = {
            'id': str(uuid.uuid4()),
            'name': name,
            'filename': filename,
            'created_at': datetime.now().isoformat()
        }
        
        tabs.append(new_tab)
        self.save_tabs(tabs)
        
        # Create empty wishlist file
        wishlist_path = os.path.join(Config.DATA_FOLDER, filename)
        with open(wishlist_path, 'w') as f:
            yaml.safe_dump([], f)
        
        return new_tab
    
    def rename_tab(self, tab_id: str, new_name: str) -> bool:
        """Rename a wishlist tab."""
        tabs = self.get_tabs()
        
        for tab in tabs:
            if tab['id'] == tab_id:
                tab['name'] = new_name
                self.save_tabs(tabs)
                return True
        
        return False
    
    def delete_tab(self, tab_id: str) -> bool:
        """Delete a wishlist tab and its data file."""
        tabs = self.get_tabs()
        
        # Don't allow deleting the last tab
        if len(tabs) <= 1:
            return False
        
        for i, tab in enumerate(tabs):
            if tab['id'] == tab_id:
                # Delete the wishlist file
                wishlist_path = os.path.join(Config.DATA_FOLDER, tab['filename'])
                if os.path.exists(wishlist_path):
                    os.remove(wishlist_path)
                
                # Remove tab from config
                tabs.pop(i)
                self.save_tabs(tabs)
                return True
        
        return False
    
    def get_wishlist_manager(self, tab_id: str) -> Optional['SingleWishlistManager']:
        """Get a wishlist manager for a specific tab."""
        tabs = self.get_tabs()
        
        for tab in tabs:
            if tab['id'] == tab_id:
                return SingleWishlistManager(tab['filename'])
        
        return None

class SingleWishlistManager:
    """Manages a single wishlist file (used by MultiWishlistManager)."""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.wishlist_path = os.path.join(Config.DATA_FOLDER, filename)
        self._ensure_wishlist_file()
    
    def _ensure_wishlist_file(self):
        """Create an empty wishlist file if it doesn't exist."""
        if not os.path.exists(self.wishlist_path):
            with open(self.wishlist_path, 'w') as f:
                yaml.safe_dump([], f)
    
    def load_wishlist(self) -> List[WishlistItem]:
        """Load the wishlist from the YAML file, excluding deleted items."""
        try:
            with open(self.wishlist_path, 'r') as f:
                data = yaml.safe_load(f) or []
                items = [WishlistItem.from_dict(item) for item in data]
                # Filter out deleted items
                active_items = [item for item in items if not item.deleted]
                # Sort by order field
                return sorted(active_items, key=lambda x: x.order)
        except Exception as e:
            print(f"Error loading wishlist: {e}")
            return []
    
    def load_all_wishlist_items(self) -> List[WishlistItem]:
        """Load all wishlist items from the YAML file, including deleted ones."""
        try:
            with open(self.wishlist_path, 'r') as f:
                data = yaml.safe_load(f) or []
                items = [WishlistItem.from_dict(item) for item in data]
                # Sort by order field
                return sorted(items, key=lambda x: x.order)
        except Exception as e:
            print(f"Error loading all wishlist items: {e}")
            return []
    
    def save_wishlist(self, wishlist: List[WishlistItem]):
        """Save the wishlist to the YAML file."""
        try:
            data = [item.to_dict() for item in wishlist]
            with open(self.wishlist_path, 'w') as f:
                yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"Error saving wishlist: {e}")
            raise
    
    def get_all_items(self) -> List[Dict]:
        """Get all wishlist items as dictionaries."""
        wishlist = self.load_wishlist()
        return [item.to_dict() for item in wishlist]
    
    def add_item(self, title: str, image: str = None, weblink: str = None) -> Dict:
        """Add a new item to the wishlist."""
        wishlist = self.load_wishlist()
        # Set order to be last
        max_order = max([item.order for item in wishlist], default=-1)
        new_item = WishlistItem(title=title, image=image, weblink=weblink, order=max_order + 1)
        wishlist.append(new_item)
        self.save_wishlist(wishlist)
        return new_item.to_dict()
    
    def update_item(self, item_id: str, title: str = None, image: str = None, weblink: str = None) -> Optional[Dict]:
        """Update an existing wishlist item."""
        all_items = self.load_all_wishlist_items()
        
        for item in all_items:
            if item.id == item_id and not item.deleted:
                if title is not None:
                    item.title = title
                if image is not None:
                    item.image = image
                if weblink is not None:
                    item.weblink = weblink
                
                self.save_wishlist(all_items)
                return item.to_dict()
        
        return None
    
    def delete_item(self, item_id: str) -> bool:
        """Soft delete an item from the wishlist by marking it as deleted."""
        all_items = self.load_all_wishlist_items()
        item_found = False
        
        for item in all_items:
            if item.id == item_id and not item.deleted:
                item.deleted = datetime.now().isoformat()
                item_found = True
                break
        
        if item_found:
            self.save_wishlist(all_items)
            return True
        
        return False
    
    def get_item(self, item_id: str) -> Optional[Dict]:
        """Get a specific item by ID."""
        wishlist = self.load_wishlist()
        
        for item in wishlist:
            if item.id == item_id:
                return item.to_dict()
        
        return None
    
    def reorder_items(self, item_ids: List[str]) -> bool:
        """Reorder items based on the provided list of item IDs."""
        try:
            all_items = self.load_all_wishlist_items()
            active_items = [item for item in all_items if not item.deleted]
            
            # Create a mapping of id to item for active items only
            items_by_id = {item.id: item for item in active_items}
            
            # Check if all provided IDs exist in active items
            if not all(item_id in items_by_id for item_id in item_ids):
                return False
            
            # Update order based on position in the list
            for i, item_id in enumerate(item_ids):
                items_by_id[item_id].order = i
            
            # Save all items (active and deleted)
            self.save_wishlist(all_items)
            return True
            
        except Exception as e:
            print(f"Error reordering items: {e}")
            return False