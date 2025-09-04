<template>
    <a-dropdown placement="bottomRight">
        <div class="user-info">
            <a-avatar :size="28">
                <template #icon>
                    <img v-if="userStore.userInfo?.avatar" :src="userStore.userInfo?.avatar" alt="">
                    <AIcon v-else type="UserOutlined"></AIcon>
                </template>
            </a-avatar>
            <span class="name">{{ userName }}</span>
        </div>
        <template #overlay>
            <a-menu @click="click">
                <a-menu-item key="userCenter">
                    <AIcon type="UserOutlined" style="margin-right: 8px;" />
                    <span>{{ $t('components.User.635192-0') }}</span>
                </a-menu-item>
                <a-sub-menu key="backend" popupClassName="backend-sub-menu">
                    <template #title>
                        <span>
                            <AIcon type="ApartmentOutlined" style="margin-right: 8px;" />
                            <span>切换服务</span>
                        </span>
                    </template>
                    <a-menu-item v-for="item in backendList" :key="item.url" :item="item">
                        <div class="backend-sub-menu-item">
                            <div class="backend-sub-menu-item-content">
                                <div class="backend-sub-menu-item-title">
                                    {{ item.name }}
                                    <a-tag v-if="item.url === active?.url" color="success" style="margin-left: 8px;">当前</a-tag>
                                </div>
                                <div class="backend-sub-menu-item-url">{{ item.url }}</div>
                            </div>
                        </div>
                    </a-menu-item>
                    <a-menu-divider />
                    <a-menu-item key="backend-manager">
                        <div style="text-align: center">
                            <AIcon type="SettingOutlined" />
                            服务管理
                        </div>
                    </a-menu-item>
                </a-sub-menu>
                <a-menu-item key="logout">
                    <AIcon type="LogoutOutlined" style="margin-right: 8px;" />
                    <span>{{ $t('components.User.635192-1') }}</span>
                </a-menu-item>
            </a-menu>
        </template>
    </a-dropdown>
</template>

<script setup lang="ts" name="HeaderUser">
import { computed } from "vue";
import { jumpLogin } from '@/router'
import { useUserStore } from '@/store/user'
import { logout } from '@/api/login'
import BackendAPI from "@/api/backend";

const backendList = ref(BackendAPI.get())
const active = ref(BackendAPI.getActive())
const userStore = useUserStore()
const router = useRouter()
const click = (e: { key: string, item: any }) => {
    switch (e.key) {
        case 'userCenter':
            router.push('/account/center')
            return;
        case 'logout':
            logout().then((resp) => {
                if (resp.success) {
                    jumpLogin()
                }
            })
            return;
        case 'backend-manager':
            router.push('/backend-manager')
            return;
        default:
            BackendAPI.setActive(e.item.props.item)
            window.location.reload()
            return
    }
}

const userName = computed(() => {
    return userStore.userInfo.name
})

</script>

<style scoped lang="less">
.user-info {
  cursor: pointer;

  .name {
    padding: 0 12px;
  }
}
</style>
