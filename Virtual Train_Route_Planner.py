from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterable


# Node definitions

@dataclass
class DLNode:
    name: str
    prev: Optional['DLNode'] = None
    next: Optional['DLNode'] = None



# Doubly Linked Route (linear line)

class DoublyLinkedRoute:
    def __init__(self, name: str):
        self.name = name
        self.head: Optional[DLNode] = None
        self.tail: Optional[DLNode] = None
        self.current: Optional[DLNode] = None

    # --- building / editing ---
    def append(self, station_name: str) -> DLNode:
        node = DLNode(station_name)
        if not self.head:
            self.head = self.tail = self.current = node
        else:
            assert self.tail is not None
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        return node

    def insert_after(self, target_name: str, station_name: str) -> bool:
        target = self.find(target_name)
        if not target:
            return False
        new_node = DLNode(station_name)
        nxt = target.next
        target.next = new_node
        new_node.prev = target
        new_node.next = nxt
        if nxt:
            nxt.prev = new_node
        else:
            self.tail = new_node
        return True

    def remove(self, station_name: str) -> bool:
        node = self.find(station_name)
        if not node:
            return False
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        if self.current is node:
            self.current = node.next or node.prev
        return True

    # --- navigation ---
    def move_forward(self) -> Optional[str]:
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.name
        return None

    def move_back(self) -> Optional[str]:
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.name
        return None

    def set_current(self, station_name: str) -> bool:
        node = self.find(station_name)
        if node:
            self.current = node
            return True
        return False

    # --- helpers ---
    def find(self, station_name: str) -> Optional[DLNode]:
        cur = self.head
        while cur:
            if cur.name.lower() == station_name.lower():
                return cur
            cur = cur.next
        return None

    def to_list(self) -> list[str]:
        out = []
        cur = self.head
        while cur:
            out.append(cur.name)
            cur = cur.next
        return out

    def __len__(self):
        return len(self.to_list())



# Circular Linked Route (loop line)

class CircularRoute:
    def __init__(self, name: str):
        self.name = name
        self.tail: Optional[DLNode] = None  # tail.next points to head
        self.current: Optional[DLNode] = None

    # --- building / editing ---
    def append(self, station_name: str) -> DLNode:
        node = DLNode(station_name)
        if not self.tail:
            # first node points to itself both ways
            node.next = node.prev = node
            self.tail = self.current = node
        else:
            head = self.tail.next
            assert head is not None
            # insert after tail, then update tail
            node.prev = self.tail
            node.next = head
            self.tail.next = node
            head.prev = node
            self.tail = node
        return node

    def insert_after(self, target_name: str, station_name: str) -> bool:
        target = self.find(target_name)
        if not target:
            return False
        new_node = DLNode(station_name)
        nxt = target.next
        target.next = new_node
        new_node.prev = target
        new_node.next = nxt
        if nxt:
            nxt.prev = new_node
        if target is self.tail:
            self.tail = new_node
        return True

    def remove(self, station_name: str) -> bool:
        node = self.find(station_name)
        if not node:
            return False
        if node.next is node and node.prev is node:
            # only one node
            self.tail = self.current = None
            return True
        # unlink
        node.prev.next = node.next
        node.next.prev = node.prev
        if self.tail is node:
            self.tail = node.prev
        if self.current is node:
            self.current = node.next
        return True

    # --- navigation ---
    def move_forward(self) -> Optional[str]:
        if self.current:
            self.current = self.current.next
            return self.current.name
        return None

    def move_back(self) -> Optional[str]:
        if self.current:
            self.current = self.current.prev
            return self.current.name
        return None

    def set_current(self, station_name: str) -> bool:
        node = self.find(station_name)
        if node:
            self.current = node
            return True
        return False

    # --- helpers ---
    def head(self) -> Optional[DLNode]:
        return None if not self.tail else self.tail.next

    def to_list(self, limit: int | None = None) -> list[str]:
        out = []
        if not self.tail:
            return out
        start = self.tail.next
        cur = start
        count = 0
        while True:
            out.append(cur.name)
            cur = cur.next
            count += 1
            if cur is start:
                break
            if limit is not None and count >= limit:
                break
        return out

    def find(self, station_name: str) -> Optional[DLNode]:
        if not self.tail:
            return None
        start = self.tail.next
        cur = start
        while True:
            if cur.name.lower() == station_name.lower():
                return cur
            cur = cur.next
            if cur is start:
                break
        return None

    def __len__(self):
        return len(self.to_list())



# Simple CLI demo (real-time navigation)

SERVICE_MIN_PER_HOP = 2  # pretend 2 minutes between adjacent stations

class Planner:
    def __init__(self):
        # seed with example lines
        self.line = DoublyLinkedRoute("Red Line")
        for s in ["Central", "Park St", "Museum", "Riverfront", "Airport"]:
            self.line.append(s)

        self.loop = CircularRoute("City Loop")
        for s in ["A1", "A2", "A3", "A4"]:
            self.loop.append(s)

    # ----- utility -----
    def eta_from(self, route, target: str) -> Optional[int]:
        if not route.current:
            return None
        # BFS not needed on linked lines; just walk
        steps_fwd = steps_back = None

        # forward steps
        steps = 0
        node = route.current
        visited_start = node
        while True:
            if node.name.lower() == target.lower():
                steps_fwd = steps
                break
            # move next (wrap automatically for circular)
            nxt = node.next if hasattr(node, 'next') else None
            if not nxt:
                # linear end reached
                break
            node = nxt
            steps += 1
            if isinstance(route, CircularRoute) and node is visited_start:
                # full loop without hit
                break

        # backward steps
        if getattr(route.current, 'prev', None) is not None:
            steps = 0
            node = route.current
            visited_start = node
            while True:
                if node.name.lower() == target.lower():
                    steps_back = steps
                    break
                prv = node.prev
                if not prv:
                    break
                node = prv
                steps += 1
                if isinstance(route, CircularRoute) and node is visited_start:
                    break

        best = None
        if steps_fwd is not None:
            best = steps_fwd
        if steps_back is not None and (best is None or steps_back < best):
            best = steps_back
        return None if best is None else best * SERVICE_MIN_PER_HOP

    # ----- menus -----
    def run(self):
        while True:
            print("\n==== Virtual Train Route Planner ====")
            print("1. Show routes")
            print("2. Navigate Linear Line (doubly linked)")
            print("3. Navigate Loop Line (circular)")
            print("4. Edit Linear Line")
            print("5. Edit Loop Line")
            print("6. Exit")
            c = input("Choose: ")
            if c == '1':
                self.show_routes()
            elif c == '2':
                self.nav_linear()
            elif c == '3':
                self.nav_loop()
            elif c == '4':
                self.edit_linear()
            elif c == '5':
                self.edit_loop()
            elif c == '6':
                print("Goodbye!")
                break
            else:
                print("Invalid option.")

    def show_routes(self):
        print(f"\n{self.line.name} (linear): {' <-> '.join(self.line.to_list())}")
        curL = self.line.current.name if self.line.current else 'None'
        print(f"Current @ {curL}")
        print(f"{self.loop.name} (loop): {' -> '.join(self.loop.to_list())} -> (back to start)")
        curC = self.loop.current.name if self.loop.current else 'None'
        print(f"Current @ {curC}")

    def nav_linear(self):
        while True:
            cur = self.line.current.name if self.line.current else 'None'
            print(f"\n[Linear] Current: {cur}")
            print("1. Next  2. Back  3. Jump to station  4. ETA to station  5. Back to main")
            c = input("Choose: ")
            if c == '1':
                name = self.line.move_forward()
                print(f"Moved to: {name}" if name else "Reached end; can't move forward.")
            elif c == '2':
                name = self.line.move_back()
                print(f"Moved to: {name}" if name else "At start; can't move back.")
            elif c == '3':
                target = input("Station name: ")
                print("OK" if self.line.set_current(target) else "Not found.")
            elif c == '4':
                target = input("Station name: ")
                eta = self.eta_from(self.line, target)
                print(f"ETA to {target}: {eta} min" if eta is not None else "Station not reachable from here.")
            elif c == '5':
                break
            else:
                print("Invalid option.")

    def nav_loop(self):
        while True:
            cur = self.loop.current.name if self.loop.current else 'None'
            print(f"\n[Loop] Current: {cur}")
            print("1. Next  2. Back  3. Jump to station  4. ETA to station  5. Spin k steps  6. Back to main")
            c = input("Choose: ")
            if c == '1':
                name = self.loop.move_forward()
                print(f"Moved to: {name}" if name else "No stations.")
            elif c == '2':
                name = self.loop.move_back()
                print(f"Moved to: {name}" if name else "No stations.")
            elif c == '3':
                target = input("Station name: ")
                print("OK" if self.loop.set_current(target) else "Not found.")
            elif c == '4':
                target = input("Station name: ")
                eta = self.eta_from(self.loop, target)
                print(f"ETA to {target}: {eta} min" if eta is not None else "Station not found.")
            elif c == '5':
                try:
                    k = int(input("Steps to move forward (+) or back (-): "))
                except ValueError:
                    print("Enter an integer.")
                    continue
                if not self.loop.current:
                    print("No stations.")
                    continue
                if k >= 0:
                    for _ in range(k):
                        self.loop.move_forward()
                else:
                    for _ in range(-k):
                        self.loop.move_back()
                print(f"Now at: {self.loop.current.name}")
            elif c == '6':
                break
            else:
                print("Invalid option.")

    def edit_linear(self):
        while True:
            print("\n[Edit Linear]")
            print("1. Add at end  2. Insert after  3. Remove  4. Back")
            c = input("Choose: ")
            if c == '1':
                s = input("Station name: ")
                self.line.append(s)
            elif c == '2':
                t = input("After which station: ")
                s = input("New station name: ")
                print("OK" if self.line.insert_after(t, s) else "Target not found.")
            elif c == '3':
                s = input("Station to remove: ")
                print("Removed" if self.line.remove(s) else "Not found.")
            elif c == '4':
                break
            else:
                print("Invalid option.")

    def edit_loop(self):
        while True:
            print("\n[Edit Loop]")
            print("1. Add at end  2. Insert after  3. Remove  4. Back")
            c = input("Choose: ")
            if c == '1':
                s = input("Station name: ")
                self.loop.append(s)
            elif c == '2':
                t = input("After which station: ")
                s = input("New station name: ")
                print("OK" if self.loop.insert_after(t, s) else "Target not found.")
            elif c == '3':
                s = input("Station to remove: ")
                print("Removed" if self.loop.remove(s) else "Not found.")
            elif c == '4':
                break
            else:
                print("Invalid option.")


if __name__ == '__main__':
    Planner().run()

