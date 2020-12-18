<template>
  <Row :gutter="10">
    <div>
      <Card>
        Online training and prediction are still under development. This page only shows the results of demand
        prediction, please refer to <a
        href="https://dl3.pushbulletusercontent.com/txU2R1QVSTLKFkO1q0CIUEV4Y9f8VpBQ/Ji%20%E7%AD%89%E3%80%82%20-%202020%20-%20How%20Does%20Dockless%20Bike-Sharing%20System%20Behave%20by%20In.pdf">relevant
        paper </a>for detailed methodology.
      </Card>
    </div>
    <Table :columns="columns" :data="data"></Table>
  </Row>
</template>

<script>
import { getArrayFromFile, getTableDataFromArray } from '@/libs/util'
import { getTableData } from '@/api/data'

export default {
  name: 'update_table_page',
  data () {
    return {
      columns: [
        {
          title: 'ID',
          key: 'id',
          minWidth: 100
        },
        {
          title: 'rent (8:00-8:15)',
          key: 'pred_rent_01',
          className: 'long-col',
          minWidth: 150
        },
        {
          title: 'return (8:00-8:15)',
          key: 'pred_return_01',
          className: 'long-col',
          minWidth: 150
        },
        {
          title: 'rent (8:15-8:30)',
          key: 'pred_rent_02',
          className: 'long-col',
          minWidth: 150
        },
        {
          title: 'return (8:15-8:30)',
          key: 'pred_return_02',
          className: 'long-col',
          minWidth: 150
        },
        {
          title: 'rent (8:30-8:45)',
          key: 'pred_rent_03',
          className: 'long-col',
          minWidth: 150
        },
        {
          title: 'return (8:30-8:45)',
          key: 'pred_return_03',
          className: 'long-col',
          minWidth: 150
        },
        {
          title: 'rent (8:45-9:00)',
          key: 'pred_rent_04',
          className: 'long-col',
          minWidth: 150
        },
        {
          title: 'return (8:45-9:00)',
          key: 'pred_return_04',
          className: 'long-col',
          minWidth: 150
        }
      ],
      data: this.data
    }
  },
  methods: {
    beforeUpload (file) {
      getArrayFromFile(file).then(data => {
        let { columns, tableData } = getTableDataFromArray(data)
        this.columns = columns
        this.tableData = tableData
      }).catch(() => {
        this.$Notice.warning({
          title: '只能上传Csv文件',
          desc: '只能上传Csv文件，请重新上传'
        })
      })
      return false
    }
  },
  created () {
    getTableData('predicted_info').then(res => {
      this.data = res.data
    }).catch(err => {
      console.log(err)
    })
  }
}
</script>

<style>
.update-table-intro {
  margin-top: 10px;
}

.code-high-line {
  color: #2d8cf0;
}


</style>
