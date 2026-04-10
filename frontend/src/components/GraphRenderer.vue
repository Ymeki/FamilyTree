<template>
  <div id="graph-container">
    <svg ref="svg" :width="width" :height="height"></svg>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue';
import * as d3 from 'd3';

export default defineComponent({
  name: 'GraphRenderer',
  props: {
    graphData: {
      type: Object,
      required: true
    },
    width: {
      type: Number,
      default: 800
    },
    height: {
      type: Number,
      default: 600
    }
  },
  setup(props) {
    const svg = ref<SVGSVGElement | null>(null);

    const drawGraph = () => {
      if (!svg.value || !props.graphData) return;

      const { nodes, links } = props.graphData;

      // Clear previous graph
      d3.select(svg.value).selectAll('*').remove();

      const simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink().id((d: any) => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(props.width / 2, props.height / 2));

      const link = d3.select(svg.value)
        .selectAll('.link')
        .data(links)
        .enter().append('line')
        .attr('class', 'link')
        .attr('stroke', '#999')
        .attr('stroke-width', 2);

      const node = d3.select(svg.value)
        .selectAll('.node')
        .data(nodes)
        .enter().append('g')
        .attr('class', 'node')
        .call(d3.drag()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended));

      node.append('circle')
        .attr('r', 5)
        .attr('fill', '#69b3a2');

      node.append('text')
        .attr('dy', -3)
        .attr('x', 6)
        .text((d: any) => d.name);

      simulation
        .nodes(nodes)
        .on('tick', () => {
          link.attr('x1', (d: any) => d.source.x)
              .attr('y1', (d: any) => d.source.y)
              .attr('x2', (d: any) => d.target.x)
              .attr('y2', (d: any) => d.target.y);

          node.attr('transform', (d: any) => `translate(${d.x},${d.y})`);
        });

      simulation.force<d3.ForceLink<any, any>>('link')!.links(links);
    };

    onMounted(() => {
      drawGraph();
    });

    watch(() => props.graphData, () => {
      drawGraph();
    });

    const dragstarted = (event: any, d: any) => {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    };

    const dragged = (event: any, d: any) => {
      d.fx = event.x;
      d.fy = event.y;
    };

    const dragended = (event: any, d: any) => {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    };

    return {
      svg
    };
  }
});
</script>

<style scoped>
#graph-container {
  border: 1px solid #ccc;
  overflow: hidden;
}
.link {
  stroke: #999;
  stroke-opacity: 0.6;
}
.node circle {
  stroke: #fff;
  stroke-width: 1.5px;
}
.node text {
  font: 10px sans-serif;
}
</style>