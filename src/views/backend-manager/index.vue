<template>
    <div class="backend-manager">
        <a-page-header title="服务管理" @back="() => router.back()" />
        <div class="backend-manager-content">
            <a-card title="服务列表" class="backend-manager-card">
                <template #extra>
                    <a-button type="primary" @click="visible = true">新增</a-button>
                </template>
                <a-table :columns="columns" :data-source="backendList" :pagination="false" row-key="url">
                    <template #bodyCell="{ column, record }">
                        <template v-if="column.key === 'action'">
                            <a-popconfirm title="确认删除？" @confirm="handleDelete(record)">
                                <a-button type="link">删除</a-button>
                            </a-popconfirm>
                        </template>
                        <template v-if="column.key === 'active'">
                            <a-tag v-if="record.url === active?.url" color="success">当前</a-tag>
                        </template>
                    </template>
                </a-table>
            </a-card>
        </div>
        <a-modal v-model:visible="visible" title="新增服务" @ok="handleOk">
            <a-form ref="formRef" :model="formState" :rules="rules">
                <a-form-item label="名称" name="name">
                    <a-input v-model:value="formState.name" />
                </a-form-item>
                <a-form-item label="地址" name="url">
                    <a-input v-model:value="formState.url" />
                </a-form-item>
            </a-form>
        </a-modal>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import BackendAPI from '@/api/backend';
import { onlyMessage } from '@jetlinks-web/utils';

const router = useRouter();
const backendList = ref(BackendAPI.get());
const active = ref(BackendAPI.getActive());
const visible = ref(false);
const formRef = ref();
const formState = reactive({
    name: '',
    url: '',
});

const rules = {
    name: [{ required: true, message: '请输入名称' }],
    url: [{ required: true, message: '请输入地址' }],
};

const columns = [
    { title: '名称', dataIndex: 'name', key: 'name' },
    { title: '地址', dataIndex: 'url', key: 'url' },
    { title: '当前', key: 'active', width: 100 },
    { title: '操作', key: 'action', width: 100 },
];

const handleDelete = (record: any) => {
    BackendAPI.remove(record.url);
    backendList.value = BackendAPI.get();
    onlyMessage('删除成功');
};

const handleOk = () => {
    formRef.value.validate().then(() => {
        BackendAPI.add(formState);
        backendList.value = BackendAPI.get();
        onlyMessage('新增成功');
        visible.value = false;
        formRef.value.resetFields();
    });
};
</script>

<style lang="less" scoped>
.backend-manager {
    .backend-manager-content {
        padding: 24px;
    }
}
</style>
