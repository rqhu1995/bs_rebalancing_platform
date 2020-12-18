<template>
  <Row :gutter="16">
    <Row type="flex" justify="center">
      <Col span="6">
        <Button :size="buttonSize" type="primary" v-on:click="filter_stations">
          <Icon type="ios-funnel"/>
          filter stations without demand
        </Button>
      </Col>
      <Col span="8">
        <Button :size="buttonSize" type="primary">
          <Icon type="md-alert"/>
          calculate priority of stations
        </Button>
      </Col>
      <Col span="5">
        <Button :size="buttonSize" type="primary">
          <Icon type="md-arrow-dropup"/>
          sort by priority
        </Button>
      </Col>
      <Col span="5">
        <Button :size="buttonSize" type="primary">
          <Icon type="md-refresh"/>
          revert from beginning
        </Button>
      </Col>
    </Row>
    <br>
    <Row>
      <Table :columns="columns" :data="this.tableData"></Table>
    </Row>
  </Row>

</template>

<script>

import PasteEditor from '_c/paste-editor'
import { getTableDataFromArray } from '@/libs/util'
import { getTableData } from '@/api/data'

export default {
  name: 'update_paste_page',
  components: {
    PasteEditor
  },
  data () {
    return {
      columns: [
        {
          title: 'station ID',
          key: 'id'
        },
        {
          title: 'docks',
          key: 'max_capacity'
        },
        {
          title: 'current bikes',
          key: 'bike_count'
        },
        {
          title: 'bike-dock ratio',
          key: 'ratio'
        },

        {
          title: 'var rate (bike/min)',
          key: 'velocity'
        },
        {
          title: 'full/empty time',
          key: 'full_empty_time'
        },
        {
          title: 'rebalancing amount',
          key: 'demand'
        }
      ],
      tableData: [],
      buttonSize: 'large'
    }
  },
  created () {
    getTableData('station_info').then(res => {
      this.tableData = res.data
      console.log(Object.keys(this.tableData[0]))
    }).catch(err => {
      console.log(err)
    })
  },
  methods: {
    filter_stations () {
      let filtered = []
      for (const record of this.tableData) {
        if (record['demand'] !== 0) {
          filtered.push(record)
        }
      }
      this.tableData = filtered
    },
    handleSuccess () {
      this.validated = true
    },
    handleError (index) {
      this.validated = false
      this.errorIndex = index
    },
    handleShow () {
      if (!this.validated) {
        this.$Notice.error({
          title: '您的内容不规范',
          desc: `您的第${this.errorIndex + 1}行数据不规范，请修改`
        })
      } else {
        let { columns, tableData } = getTableDataFromArray(this.pasteDataArr)
        this.columns = columns
        this.tableData = tableData
      }
    }
  }
}
</script>

<style lang="less">
.update-paste {
  &-con {
    height: 350px;
  }

  &-btn-con {
    box-sizing: content-box;
    height: 30px;
    padding: 15px 0 5px;
  }
}

.paste-tip {
  color: #19be6b;
}
</style>
