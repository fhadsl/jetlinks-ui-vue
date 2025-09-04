class BackendAPI {
    private backendKey = 'backend_list';
    private activeKey = 'active_backend';

    get(): Record<string, any>[] {
        const value = localStorage.getItem(this.backendKey);
        if (value) {
            try {
                return JSON.parse(value);
            } catch (e) {
                return [];
            }
        }
        return [];
    }

    set(data: Record<string, any>[]) {
        localStorage.setItem(this.backendKey, JSON.stringify(data));
    }

    add(data: Record<string, any>) {
        const list = this.get();
        const oldLlist = list.filter(item => item.url !== data.url)
        this.set([...oldLlist, data]);
    }

    remove(url: string) {
        const list = this.get();
        const newList = list.filter((item) => item.url !== url);
        this.set(newList);
    }

    getActive(): Record<string, any> | undefined {
        const value = localStorage.getItem(this.activeKey);
        if (value) {
            try {
                return JSON.parse(value);
            } catch (e) {
                return undefined;
            }
        }
        return undefined;
    }

    setActive(data: Record<string, any>) {
        localStorage.setItem(this.activeKey, JSON.stringify(data));
    }

    removeActive() {
        localStorage.removeItem(this.activeKey);
    }
}

export default new BackendAPI();
