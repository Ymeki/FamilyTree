<template>
  <div class="member-form">
    <h2>{{ isEdit ? '编辑成员' : '添加成员' }}</h2>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="name">姓名:</label>
        <input type="text" v-model="member.name" required />
      </div>
      <div>
        <label for="gender">性别:</label>
        <select v-model="member.gender" required>
          <option value="male">男</option>
          <option value="female">女</option>
          <option value="other">其他</option>
        </select>
      </div>
      <div>
        <label for="birth_date">出生日期:</label>
        <input type="date" v-model="member.birth_date" />
      </div>
      <div>
        <label for="death_date">去世日期:</label>
        <input type="date" v-model="member.death_date" />
      </div>
      <div>
        <label for="bio">简介:</label>
        <textarea v-model="member.bio"></textarea>
      </div>
      <div>
        <label for="custom_data">自定义字段:</label>
        <textarea v-model="member.custom_data" placeholder='{"key": "value"}'></textarea>
      </div>
      <div>
        <label for="father_id">父亲ID:</label>
        <input type="text" v-model="member.father_id" />
      </div>
      <div>
        <label for="mother_id">母亲ID:</label>
        <input type="text" v-model="member.mother_id" />
      </div>
      <button type="submit">{{ isEdit ? '更新成员' : '添加成员' }}</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, PropType } from 'vue';

export default defineComponent({
  name: 'MemberForm',
  props: {
    initialMember: {
      type: Object as PropType<{
        name: string;
        gender: string;
        birth_date?: string;
        death_date?: string;
        bio?: string;
        custom_data?: string;
        father_id?: string;
        mother_id?: string;
      }>,
      default: () => ({}),
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const member = ref({ ...props.initialMember });

    const handleSubmit = () => {
      // Handle form submission logic here
      console.log('Submitted member data:', member.value);
    };

    return {
      member,
      handleSubmit,
    };
  },
});
</script>

<style scoped>
.member-form {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.member-form h2 {
  text-align: center;
}

.member-form div {
  margin-bottom: 15px;
}

.member-form label {
  display: block;
  margin-bottom: 5px;
}

.member-form input,
.member-form select,
.member-form textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>