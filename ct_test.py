from ct_scheduler import Scheduler

def main():
    scheduler = Scheduler(lambda: None, lambda x: x)
    scheduler.add(3, print, "hello")
    scheduler.add(3, scheduler.add, 3, print, "world")
    scheduler.run()


if __name__ == '__main__':
    main()